"""Read the saved V01 field and quantify the geometry-driven turn problem.

This is a read-only Phase 8 diagnostic. It does not modify V01 and does not
generate a proposed geometry. Run with ParaView's pvpython in WSL.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkCellCenters
from vtkmodules.vtkFiltersVerdict import vtkCellSizeFilter


ROOT = Path(__file__).resolve().parents[2]
CASE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "cfd/V01_fan"
OUT = ROOT / "results/GEOMETRY_OPTIMIZATION"
OUT.mkdir(parents=True, exist_ok=True)
RHO = 1.20


def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for index in range(dataset.GetNumberOfBlocks()):
            block = dataset.GetBlock(index)
            if block is not None:
                yield from leaves(block)
    elif dataset.GetNumberOfCells():
        yield dataset


def cell_volumes(dataset):
    sizes = vtkCellSizeFilter()
    sizes.SetInputData(dataset)
    sizes.Update()
    return vtk_to_numpy(sizes.GetOutput().GetCellData().GetArray("Volume"))


times = sorted(
    (path for path in CASE.iterdir() if path.is_dir() and path.name.replace(".", "", 1).isdigit()),
    key=lambda path: float(path.name),
)
final = times[-1]
reader = OpenFOAMReader(FileName=str(CASE / "V01.foam"))
reader.MeshRegions = ["internalMesh"]
reader.CellArrays = ["U", "p"]
reader.UpdatePipeline(time=float(final.name))
grid = list(leaves(servermanager.Fetch(reader)))[0]

vol = cell_volumes(grid)
u = vtk_to_numpy(grid.GetCellData().GetArray("U"))
p_pa = vtk_to_numpy(grid.GetCellData().GetArray("p")) * RHO
speed = np.linalg.norm(u, axis=1)
centres = vtkCellCenters()
centres.SetInputData(grid)
centres.Update()
xyz = vtk_to_numpy(centres.GetOutput().GetPoints().GetData())


def inside(bounds):
    """Strict cell-centre mask for [xmin,xmax,ymin,ymax,zmin,zmax]."""
    return (
        (xyz[:, 0] > bounds[0]) & (xyz[:, 0] < bounds[1])
        & (xyz[:, 1] > bounds[2]) & (xyz[:, 1] < bounds[3])
        & (xyz[:, 2] > bounds[4]) & (xyz[:, 2] < bounds[5])
    )


riser = inside([0.320, 0.690, 0.150, 0.650, 0.850, 2.000])
plenum = inside([0.320, 0.500, 0.100, 0.700, 0.150, 0.850])
riser_reverse = riser & (u[:, 2] < -0.05)
plenum_reverse = plenum & (u[:, 0] < -0.05)
common_riser = riser & (xyz[:, 2] < 1.850)


def weighted_mean(values, mask):
    return float(np.average(values[mask], weights=vol[mask]))


def weighted_fraction(mask, reference):
    return float(vol[mask].sum() / vol[reference].sum())


height_rows = []
z_edges = np.linspace(0.850, 2.000, 24)
for lo, hi in zip(z_edges[:-1], z_edges[1:]):
    band = riser & (xyz[:, 2] >= lo) & (xyz[:, 2] < hi)
    if not band.any():
        continue
    height_rows.append({
        "z_mid_m": float((lo + hi) / 2),
        "reverse_volume_fraction_Uz_below_minus_0p05": weighted_fraction(band & (u[:, 2] < -0.05), band),
        "mean_Uz_m_s": weighted_mean(u[:, 2], band),
        "mean_speed_m_s": weighted_mean(speed, band),
        "min_Uz_m_s": float(u[band, 2].min()),
        "max_Uz_m_s": float(u[band, 2].max()),
    })

x_rows = []
x_edges = np.linspace(0.320, 0.690, 20)
for lo, hi in zip(x_edges[:-1], x_edges[1:]):
    band = riser & (xyz[:, 0] >= lo) & (xyz[:, 0] < hi)
    if not band.any():
        continue
    x_rows.append({
        "x_mid_m": float((lo + hi) / 2),
        "reverse_volume_fraction_Uz_below_minus_0p05": weighted_fraction(band & (u[:, 2] < -0.05), band),
        "mean_Uz_m_s": weighted_mean(u[:, 2], band),
    })

reverse_xyz = xyz[riser_reverse]
reverse_weights = vol[riser_reverse]
reverse_centroid = np.average(reverse_xyz, axis=0, weights=reverse_weights)
max_index = int(np.argmax(speed))

diagnosis = {
    "label": "SIMULATION — V01 FIELD DIAGNOSIS | EMPTY TOWER | PARTIAL / NON-CONVERGED",
    "source_case": str(CASE),
    "final_iteration": float(final.name),
    "definitions": {
        "riser_reverse": "CLEAN_RISER cells with Uz < -0.05 m/s (same as V01)",
        "clean_plenum_reverse": "CLEAN_PLENUM cells with Ux < -0.05 m/s (same as V01)",
        "low_speed": "All fluid cells with |U| < 0.1 m/s (same as V01)",
    },
    "geometry_facts": {
        "lower_crossflow_area_m2": 0.420,
        "riser_entry_opening_area_m2": 0.090,
        "riser_area_m2": 0.185,
        "lower_to_entry_contraction_ratio": 0.420 / 0.090,
        "entry_to_riser_expansion_ratio": 0.185 / 0.090,
        "turn_angle_degrees": 90,
    },
    "field_findings": {
        "riser_reverse_volume_fraction": weighted_fraction(riser_reverse, riser),
        "common_riser_z0p85_to_1p85_reverse_volume_fraction": weighted_fraction(
            common_riser & (u[:, 2] < -0.05), common_riser
        ),
        "clean_plenum_reverse_volume_fraction": weighted_fraction(plenum_reverse, plenum),
        "low_speed_total_volume_fraction": float(vol[speed < 0.1].sum() / vol.sum()),
        "reverse_cell_minimum_center_z_m": float(reverse_xyz[:, 2].min()),
        "reverse_cell_maximum_center_z_m": float(reverse_xyz[:, 2].max()),
        "reverse_region_centroid_m": reverse_centroid.tolist(),
        "maximum_speed_m_s": float(speed[max_index]),
        "maximum_speed_cell_center_m": xyz[max_index].tolist(),
        "maximum_speed_pressure_Pa": float(p_pa[max_index]),
        "riser_entry_first_0p05m_reverse_fraction": height_rows[0]["reverse_volume_fraction_Uz_below_minus_0p05"],
        "riser_entry_first_0p05m_mean_Uz_m_s": height_rows[0]["mean_Uz_m_s"],
    },
    "riser_by_height": height_rows,
    "riser_by_x": x_rows,
    "interpretation": (
        "Reverse Uz begins in the first cell layer above the riser entrance and occupies a large "
        "fraction of the entrance band. Its coincidence with the 4.67:1 contraction, abrupt 90-degree "
        "turn and 2.06:1 expansion supports a geometry-driven separation diagnosis. Because V01 is "
        "not fully converged and no transient or mesh study exists, this is evidence of association, "
        "not proof of a unique physical cause."
    ),
}
(OUT / "v01_diagnosis.json").write_text(json.dumps(diagnosis, indent=2), encoding="utf-8")

# Chart contract: quantify whether the reverse-flow indicator originates at the turn
# and whether it decays with height. Static PNG is the requested durable report surface.
fig, ax1 = plt.subplots(figsize=(8.8, 5.0), layout="constrained")
z = np.array([row["z_mid_m"] for row in height_rows])
reverse_pct = np.array([row["reverse_volume_fraction_Uz_below_minus_0p05"] for row in height_rows]) * 100
mean_uz = np.array([row["mean_Uz_m_s"] for row in height_rows])
ax1.barh(z, reverse_pct, height=0.040, color="#3569a8", edgecolor="#23384d", linewidth=0.6)
ax1.set(xlabel="Reverse-flow volume in 50 mm riser band (%)", ylabel="Height z (m)", xlim=(0, max(35, reverse_pct.max() * 1.08)))
ax1.grid(axis="x", alpha=0.20)
ax2 = ax1.twiny()
ax2.plot(mean_uz, z, color="#ae7927", marker="o", markersize=3.2, linewidth=1.2)
ax2.set_xlabel("Volume-weighted mean Uz (m/s)")
ax1.set_title("V01 riser reverse-flow indicator by height\nSaved iteration 4000; Uz < -0.05 m/s; PARTIAL / NON-CONVERGED")
fig.savefig(OUT / "v01_riser_reverse_by_height.png", dpi=180)
plt.close(fig)

# Actual cell-centre vector inspection on the nearest saved central Y layer.
y_layer = np.unique(np.round(xyz[:, 1], 8))[np.argmin(np.abs(np.unique(np.round(xyz[:, 1], 8)) - 0.4))]
plane = np.isclose(xyz[:, 1], y_layer, atol=1e-7)
px, pz = xyz[plane, 0], xyz[plane, 2]
pu = u[plane]
ps = speed[plane]
order = np.lexsort((px, pz))
px, pz, pu, ps = px[order], pz[order], pu[order], ps[order]
fig, ax = plt.subplots(figsize=(7.2, 9.2), layout="constrained")
points = ax.scatter(px, pz, c=ps, cmap="viridis", s=18, marker="s", linewidths=0, vmin=0, vmax=float(speed.max()))
reverse_plane = pu[:, 2] < -0.05
ax.scatter(px[reverse_plane], pz[reverse_plane], facecolors="none", edgecolors="#b24c3a", s=23, linewidths=0.8, label="Uz < -0.05 m/s")
sample = np.arange(0, len(px), 8)
ax.quiver(px[sample], pz[sample], pu[sample, 0], pu[sample, 2], color="#20262e", angles="xy", scale_units="xy", scale=30, width=0.0022, alpha=0.85)
ax.axhline(0.850, color="#5f6873", linestyle="--", linewidth=0.9)
ax.text(0.015, 0.872, "riser entrance z=0.850 m", fontsize=8, color="#333333")
ax.set(xlabel="X (m)", ylabel="Z (m)", xlim=(-0.02, 0.72), ylim=(0.10, 2.03), aspect="equal")
ax.set_title(f"V01 central-layer velocity vectors and speed\nY={y_layer:.3f} m; saved iteration 4000; PARTIAL / NON-CONVERGED")
ax.legend(loc="lower right", fontsize=8)
bar = fig.colorbar(points, ax=ax, fraction=0.046, pad=0.04)
bar.set_label("Cell-centre speed (m/s)")
fig.savefig(OUT / "v01_turn_vector_diagnosis.png", dpi=180)
plt.close(fig)

print(json.dumps(diagnosis, indent=2))
