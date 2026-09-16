"""Generate exact, comparable OpenFOAM cases from the three Phase 8 CAD files.

Run with FreeCAD's Python. Existing solved cases are protected. All stage zones
remain empty air, and the KVO 250 terminal suction model is copied unchanged.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import shutil
from pathlib import Path

import FreeCAD as App
import Part


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "cfd" / "V01_fan"
CELL_MM = 20.0
NOTICE = "DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT"
SOURCES = {
    "GEO_A": ROOT / "cad/parametric/AQI_Tower_ConceptA_GEO_A.FCStd",
    "GEO_B": ROOT / "cad/parametric/AQI_Tower_ConceptA_GEO_B.FCStd",
    "GEO_C": ROOT / "cad/parametric/AQI_Tower_ConceptA_GEO_C.FCStd",
}


def header(name, cls="dictionary"):
    return f"FoamFile {{ version 2.0; format ascii; class {cls}; object {name}; }}\n"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numeric_solution_directories(case):
    return [
        path for path in case.iterdir()
        if path.is_dir() and re.fullmatch(r"\d+(?:\.\d+)?", path.name) and float(path.name) > 0
    ] if case.exists() else []


def copy_case_physics(case):
    shutil.copytree(BASE / "0", case / "0", dirs_exist_ok=True)
    # lnInclude contains WSL symbolic links that Windows cannot copy directly;
    # it is not needed when loading the already compiled, source-matched library.
    shutil.copytree(
        BASE / "dynamicCode",
        case / "dynamicCode",
        ignore=shutil.ignore_patterns("lnInclude"),
        dirs_exist_ok=True,
    )
    (case / "constant").mkdir(parents=True)
    for path in (BASE / "constant").iterdir():
        if path.is_file():
            shutil.copy2(path, case / "constant" / path.name)
    (case / "system").mkdir(parents=True)
    shutil.copy2(BASE / "system/fvSchemes", case / "system/fvSchemes")
    shutil.copy2(BASE / "logs/initial_kvo_setup/fvSolution", case / "system/fvSolution.initial")
    shutil.copy2(BASE / "system/fvSolution", case / "system/fvSolution.tight")
    shutil.copy2(case / "system/fvSolution.initial", case / "system/fvSolution")
    control = (BASE / "system/controlDict").read_text(encoding="utf-8")
    control = re.sub(r"startFrom\s+\w+\s*;", "startFrom startTime;", control)
    control = re.sub(r"endTime\s+\d+\s*;", "endTime 3000;", control)
    (case / "system/controlDict").write_text(control, encoding="utf-8")
    (case / "logs").mkdir(parents=True)


def read_boxes(source):
    doc = App.openDocument(str(source))
    doc.recompute()
    boxes = {}
    shapes = []
    for obj in doc.Objects:
        region = getattr(obj, "CFDRegion", "")
        if not region or region == "REFERENCE_ONLY":
            continue
        shape = obj.Shape
        if not shape.isValid() or len(shape.Solids) != 1:
            raise RuntimeError(f"{source.name}: invalid single solid {obj.Name}")
        bound = shape.BoundBox
        bounds = [bound.XMin, bound.XMax, bound.YMin, bound.YMax, bound.ZMin, bound.ZMax]
        rectangle = Part.makeBox(bound.XLength, bound.YLength, bound.ZLength, App.Vector(bound.XMin, bound.YMin, bound.ZMin))
        if abs(shape.Volume - rectangle.Volume) > 1e-3 or shape.cut(rectangle).Volume + rectangle.cut(shape).Volume > 1e-3:
            raise RuntimeError(f"{source.name}: {obj.Name} is not an exact axis-aligned box")
        if region in boxes:
            raise RuntimeError(f"{source.name}: duplicate CFDRegion {region}")
        boxes[region] = {
            "object": obj.Name,
            "bounds_mm": bounds,
            "volume_m3": shape.Volume * 1e-9,
            "parameter_status": getattr(obj, "ParameterStatus", "UNKNOWN"),
        }
        shapes.append(shape)
    for left, right in itertools.combinations(shapes, 2):
        if left.common(right).Volume > 1e-3:
            raise RuntimeError(f"{source.name}: overlapping CFD volumes")
    union = shapes[0].multiFuse(shapes[1:]).removeSplitter()
    if not union.isValid() or len(union.Solids) != 1:
        raise RuntimeError(f"{source.name}: fluid regions are not one connected solid")
    if abs(union.Volume - sum(shape.Volume for shape in shapes)) > 1e-3:
        raise RuntimeError(f"{source.name}: duplicate fluid volume")
    App.closeDocument(doc.Name)
    return boxes, union.Volume * 1e-9


def create_mesh_dictionary(case, boxes):
    axes = [
        sorted({round(item["bounds_mm"][side], 8) for item in boxes.values() for side in (2 * dim, 2 * dim + 1)})
        for dim in range(3)
    ]
    occupied = {}
    for index in itertools.product(*(range(len(axis) - 1) for axis in axes)):
        centre = [(axes[dim][index[dim]] + axes[dim][index[dim] + 1]) / 2 for dim in range(3)]
        matches = [
            name for name, item in boxes.items()
            if all(item["bounds_mm"][2 * dim] < centre[dim] < item["bounds_mm"][2 * dim + 1] for dim in range(3))
        ]
        if len(matches) > 1:
            raise RuntimeError(f"Mesh partition overlap at {centre}: {matches}")
        if matches:
            occupied[index] = matches[0]

    vertices = []
    vertex_ids = {}

    def vertex(index):
        if index not in vertex_ids:
            vertex_ids[index] = len(vertices)
            vertices.append(tuple(axes[dim][index[dim]] for dim in range(3)))
        return vertex_ids[index]

    corners = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    face_definitions = [
        ((-1, 0, 0), (0, 4, 7, 3)), ((1, 0, 0), (1, 2, 6, 5)),
        ((0, -1, 0), (0, 1, 5, 4)), ((0, 1, 0), (3, 7, 6, 2)),
        ((0, 0, -1), (0, 3, 2, 1)), ((0, 0, 1), (4, 5, 6, 7)),
    ]
    boundaries = {name: [] for name in ["AIR_INLET", "AIR_OUTLET", "WALLS"]}
    boundary_areas = {name: 0.0 for name in boundaries}
    blocks = []
    cell_counts = dict.fromkeys(boxes, 0)
    for index, region in occupied.items():
        ids = [vertex(tuple(index[dim] + corner[dim] for dim in range(3))) for corner in corners]
        lengths = [axes[dim][index[dim] + 1] - axes[dim][index[dim]] for dim in range(3)]
        counts = [max(1, math.ceil(length / CELL_MM - 1e-10)) for length in lengths]
        cell_counts[region] += math.prod(counts)
        blocks.append(f"hex ({' '.join(map(str, ids))}) {region} ({' '.join(map(str, counts))}) simpleGrading (1 1 1)")
        for delta, face in face_definitions:
            neighbour = tuple(index[dim] + delta[dim] for dim in range(3))
            if neighbour in occupied:
                continue
            patch = "WALLS"
            if region == "AIR_INLET" and delta == (-1, 0, 0):
                patch = "AIR_INLET"
            elif region == "AIR_OUTLET" and delta == (1, 0, 0):
                patch = "AIR_OUTLET"
            boundaries[patch].append("(" + " ".join(str(ids[position]) for position in face) + ")")
            normal = next(dim for dim in range(3) if delta[dim])
            boundary_areas[patch] += math.prod(lengths[dim] for dim in range(3) if dim != normal) * 1e-6

    dictionary = header("blockMeshDict") + "\nconvertToMeters 0.001;\nvertices\n(\n"
    dictionary += "\n".join("(" + " ".join(f"{value:.9g}" for value in point) + ")" for point in vertices)
    dictionary += "\n);\nblocks\n(\n" + "\n".join(blocks) + "\n);\nedges ();\nboundary\n(\n"
    for name, faces in boundaries.items():
        patch_type = "wall" if name == "WALLS" else "patch"
        dictionary += f"{name}\n{{\n type {patch_type};\n faces\n(\n" + "\n".join(faces) + "\n);\n}\n"
    dictionary += ");\nmergePatchPairs ();\n"
    (case / "system/blockMeshDict").write_text(dictionary, encoding="utf-8")
    return {
        "axes_mm": axes,
        "block_count": len(blocks),
        "cell_counts": cell_counts,
        "total_cells": sum(cell_counts.values()),
        "boundary_area_m2": boundary_areas,
        "max_cell_edge_mm": CELL_MM,
    }


def main():
    fan_json = ROOT / "data/fans/systemair_KVO_250.json"
    base_p_hash = sha256(BASE / "0/p")
    base_mesh_hash = sha256(BASE / "system/fvSchemes")
    summary = {
        "notice": NOTICE,
        "fan_json": str(fan_json.relative_to(ROOT)),
        "fan_json_sha256": sha256(fan_json),
        "fan_boundary_source_sha256": base_p_hash,
        "fvSchemes_source_sha256": base_mesh_hash,
        "cases": {},
    }
    for code, source in SOURCES.items():
        case = ROOT / "cfd" / code
        if case.exists():
            if numeric_solution_directories(case):
                raise RuntimeError(f"Existing solved case protected: {case}")
            allowed_partial = {"0", "dynamicCode", "constant", "system", "logs", "geometry_audit.json", f"{code}.foam"}
            unexpected = {path.name for path in case.iterdir()} - allowed_partial
            if unexpected:
                raise RuntimeError(f"Unexpected files in unsolved case {case}: {sorted(unexpected)}")
        case.mkdir(parents=True, exist_ok=True)
        boxes, volume = read_boxes(source)
        copy_case_physics(case)
        mesh = create_mesh_dictionary(case, boxes)
        (case / f"{code}.foam").touch()
        audit = {
            "case": code,
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source),
            "freecad_version": App.Version(),
            "units": "CAD millimetres; mesh metres",
            "parameter_notice": NOTICE,
            "regions": boxes,
            "fluid_volume_m3": volume,
            "stage_treatment": "EMPTY FLUID; NO RESISTANCE",
            "fan_model": "Unchanged KVO 250 terminal suction, same orientation and six-point curve",
            "comparison_physics": "Copied from V01; initial run uses identical fvSolution and fvSchemes",
            **mesh,
        }
        (case / "geometry_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
        summary["cases"][code] = {
            "source_cad_sha256": audit["source_sha256"],
            "fluid_volume_m3": volume,
            "total_cells": mesh["total_cells"],
            "block_count": mesh["block_count"],
            "outlet_area_m2": mesh["boundary_area_m2"]["AIR_OUTLET"],
        }
        print(json.dumps({code: summary["cases"][code]}, indent=2))
    (ROOT / "cfd/PHASE8_CASE_MANIFEST.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
