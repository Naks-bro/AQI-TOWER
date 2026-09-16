"""Prepare Phase 9 GEO_C + Freudenberg H13 resistance sensitivity cases.

Run with FreeCAD's Python on Windows. GEO_C and all earlier cases are read-only.
The 593 mm square filter face is a cyclic porous baffle; the surrounding
600 x 700 mm passage is closed by a zero-thickness no-slip mounting plate.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import shutil
import sys
from pathlib import Path

import FreeCAD as App

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from prepare_phase8_geometry_cases import read_boxes


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "cfd" / "GEO_C"
SOURCE_CAD = ROOT / "cad" / "parametric" / "AQI_Tower_ConceptA_GEO_C.FCStd"
FAN_JSON = ROOT / "data" / "fans" / "systemair_KVO_250.json"
FILTER_JSON = ROOT / "data" / "filters" / "freudenberg_SF13B_593x593x292.json"
PHASE_ROOT = ROOT / "cfd" / "FILTER_H13"
CELL_MM = 20.0
RHO = 1.20
NU = 1.5e-5
FILTER_WIDTH_M = 0.593
FILTER_HEIGHT_M = 0.593
FILTER_DEPTH_M = 0.292
FILTER_AREA_REPORTED_M2 = 0.3516
FILTER_X_M = 0.305
FILTER_Y0_M = 0.1035
FILTER_Z0_M = 0.2035
CONFIRMED_DP_PA = 300.0
CONFIRMED_V_M_S = 2.84
LINEAR_SLOPE_PA_PER_M_S = CONFIRMED_DP_PA / CONFIRMED_V_M_S
SCENARIOS = {
    "CASE_L": {
        "multiplier": 80.0 / 126.0,
        "basis": "ENGINEERING SENSITIVITY: lower edge of the existing 80-150 Pa planning bracket at about 1.19 m/s; not measured",
    },
    "CASE_M": {
        "multiplier": 1.0,
        "basis": "APPROXIMATION FROM SINGLE MANUFACTURER DATA POINT: linear clean-filter relation through 300 Pa at 2.84 m/s",
    },
    "CASE_H": {
        "multiplier": 150.0 / 126.0,
        "basis": "ENGINEERING SENSITIVITY: upper edge of the existing 80-150 Pa planning bracket at about 1.19 m/s; not measured or a terminal/loading rating",
    },
}


def header(name: str, cls: str = "dictionary") -> str:
    return f"FoamFile {{ version 2.0; format ascii; class {cls}; object {name}; }}\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numeric_solution_directories(case: Path) -> list[Path]:
    if not case.exists():
        return []
    return [
        path for path in case.iterdir()
        if path.is_dir() and re.fullmatch(r"\d+(?:\.\d+)?", path.name) and float(path.name) > 0
    ]


def copy_case_physics(case: Path) -> None:
    (case / "0").mkdir(parents=True, exist_ok=True)
    for name in ["p", "U", "k", "epsilon", "nut"]:
        shutil.copy2(BASE / "0" / name, case / "0" / name)
    shutil.copytree(
        BASE / "dynamicCode",
        case / "dynamicCode",
        ignore=shutil.ignore_patterns("lnInclude"),
        dirs_exist_ok=True,
    )
    (case / "constant").mkdir(parents=True, exist_ok=True)
    for path in (BASE / "constant").iterdir():
        if path.is_file():
            shutil.copy2(path, case / "constant" / path.name)
    (case / "system").mkdir(parents=True, exist_ok=True)
    for name in ["fvSchemes", "fvSolution.initial", "fvSolution.tight"]:
        shutil.copy2(BASE / "system" / name, case / "system" / name)
    shutil.copy2(case / "system" / "fvSolution.initial", case / "system" / "fvSolution")

    control = (BASE / "system" / "controlDict").read_text(encoding="utf-8")
    control = re.sub(r"startFrom\s+\w+\s*;", "startFrom startTime;", control)
    control = re.sub(r"endTime\s+\d+\s*;", "endTime 3000;", control)
    extra = r'''
    filterFlow
    {
        type surfaceFieldValue;
        libs ("libfieldFunctionObjects.so");
        patch FILTER_UPSTREAM;
        operation orientedSum;
        fields (phi);
        writeFields false;
        writeControl timeStep;
        writeInterval 10;
        log true;
    }
    filterPressureUp
    {
        type surfaceFieldValue;
        libs ("libfieldFunctionObjects.so");
        patch FILTER_UPSTREAM;
        operation areaAverage;
        fields (p);
        writeFields false;
        writeControl timeStep;
        writeInterval 10;
        log true;
    }
    filterPressureDown
    {
        type surfaceFieldValue;
        libs ("libfieldFunctionObjects.so");
        patch FILTER_DOWNSTREAM;
        operation areaAverage;
        fields (p);
        writeFields false;
        writeControl timeStep;
        writeInterval 10;
        log true;
    }
'''
    position = control.rfind("\n}")
    if position < 0:
        raise RuntimeError("Could not locate functions closing brace in controlDict")
    control = control[:position] + extra + control[position:]
    (case / "system" / "controlDict").write_text(control, encoding="utf-8")
    (case / "logs").mkdir(parents=True, exist_ok=True)


def create_mesh_dictionary(case: Path, boxes: dict) -> dict:
    extra_axes = {
        0: [FILTER_X_M * 1000],
        1: [FILTER_Y0_M * 1000, (FILTER_Y0_M + FILTER_WIDTH_M) * 1000],
        2: [FILTER_Z0_M * 1000, (FILTER_Z0_M + FILTER_HEIGHT_M) * 1000],
    }
    axes = []
    for dim in range(3):
        values = {round(item["bounds_mm"][side], 8) for item in boxes.values() for side in (2 * dim, 2 * dim + 1)}
        values.update(extra_axes[dim])
        axes.append(sorted(values))

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
    (case / "system" / "blockMeshDict").write_text(dictionary, encoding="utf-8")
    return {
        "axes_mm": axes,
        "block_count": len(blocks),
        "cell_counts": cell_counts,
        "total_cells": sum(cell_counts.values()),
        "boundary_area_m2": boundary_areas,
        "max_cell_edge_mm": CELL_MM,
    }


def cyclic_patch_fields(darcy_d: float) -> str:
    return f'''
                p
                {{
                    type porousBafflePressure;
                    patchType cyclic;
                    D {darcy_d:.12g};
                    I 0;
                    length {FILTER_DEPTH_M};
                    relaxation 0.2;
                    jump uniform 0;
                    value uniform -50;
                }}
                U {{ type cyclic; }}
                k {{ type cyclic; }}
                epsilon {{ type cyclic; }}
                nut {{ type cyclic; }}
'''


def wall_patch_fields() -> str:
    return '''
                p { type zeroGradient; }
                U { type noSlip; }
                k { type kqRWallFunction; value uniform 0.00375; }
                epsilon { type epsilonWallFunction; value uniform 0.000834; }
                nut { type nutkWallFunction; value uniform 0; }
'''


def baffle_entry(name: str, origin: tuple[float, float, float], span: tuple[float, float, float], owner: str, neighbour: str, patch_type: str, fields: str) -> str:
    return f'''
    {name}
    {{
        type surface;
        surface plate;
        origin ({origin[0]} {origin[1]} {origin[2]});
        span ({span[0]} {span[1]} {span[2]});
        owner
        {{
            name {owner};
            type {patch_type};
            {'neighbourPatch ' + neighbour + ';' if patch_type == 'cyclic' else ''}
            patchFields
            {{
{fields}
            }}
        }}
        neighbour
        {{
            name {neighbour};
            type {patch_type};
            {'neighbourPatch ' + owner + ';' if patch_type == 'cyclic' else ''}
            patchFields
            {{
{fields}
            }}
        }}
    }}
'''


def create_baffles_dictionary(case: Path, darcy_d: float) -> None:
    entries = [
        baffle_entry(
            "filterActiveFace",
            (FILTER_X_M, FILTER_Y0_M, FILTER_Z0_M),
            (0.0, FILTER_WIDTH_M, FILTER_HEIGHT_M),
            "FILTER_UPSTREAM", "FILTER_DOWNSTREAM", "cyclic", cyclic_patch_fields(darcy_d),
        ),
        baffle_entry(
            "frameLeft",
            (FILTER_X_M, 0.100, 0.150), (0.0, FILTER_Y0_M - 0.100, 0.700),
            "FILTER_FRAME_UPSTREAM", "FILTER_FRAME_DOWNSTREAM", "wall", wall_patch_fields(),
        ),
        baffle_entry(
            "frameRight",
            (FILTER_X_M, FILTER_Y0_M + FILTER_WIDTH_M, 0.150), (0.0, 0.700 - FILTER_Y0_M - FILTER_WIDTH_M, 0.700),
            "FILTER_FRAME_UPSTREAM", "FILTER_FRAME_DOWNSTREAM", "wall", wall_patch_fields(),
        ),
        baffle_entry(
            "frameBottom",
            (FILTER_X_M, FILTER_Y0_M, 0.150), (0.0, FILTER_WIDTH_M, FILTER_Z0_M - 0.150),
            "FILTER_FRAME_UPSTREAM", "FILTER_FRAME_DOWNSTREAM", "wall", wall_patch_fields(),
        ),
        baffle_entry(
            "frameTop",
            (FILTER_X_M, FILTER_Y0_M, FILTER_Z0_M + FILTER_HEIGHT_M), (0.0, FILTER_WIDTH_M, 0.850 - FILTER_Z0_M - FILTER_HEIGHT_M),
            "FILTER_FRAME_UPSTREAM", "FILTER_FRAME_DOWNSTREAM", "wall", wall_patch_fields(),
        ),
    ]
    text = header("createBafflesDict") + "\ninternalFacesOnly true;\nfields true;\nbaffles\n{\n" + "".join(entries) + "}\n"
    (case / "system" / "createBafflesDict").write_text(text, encoding="utf-8")


def main() -> None:
    if not BASE.exists():
        raise RuntimeError("Preserved GEO_C baseline is missing")
    boxes, volume = read_boxes(SOURCE_CAD)
    phase_manifest = {
        "phase": 9,
        "geometry": "GEO_C unchanged outer fluid envelope; local mesh partitions added at the exact filter aperture",
        "source_cad": str(SOURCE_CAD.relative_to(ROOT)),
        "source_cad_sha256": sha256(SOURCE_CAD),
        "fan_json": str(FAN_JSON.relative_to(ROOT)),
        "fan_json_sha256": sha256(FAN_JSON),
        "filter_json": str(FILTER_JSON.relative_to(ROOT)),
        "filter_json_sha256": sha256(FILTER_JSON),
        "fit": {
            "available_passage_mm": [600, 700],
            "filter_face_mm": [593, 593],
            "filter_depth_mm": 292,
            "physical_envelope_bounds_mm": [159, 451, 103.5, 696.5, 203.5, 796.5],
            "stage_slot_depth_mm": 30,
            "fit_statement": "Fits the overall lower flow envelope but spans the placeholder stage bank; does not fit one 30 mm placeholder slot",
            "seal_assumption": "Perfectly sealed zero-thickness mounting plate in CFD; gasket and access hardware not designed",
        },
        "model": {
            "type": "porousBafflePressure; linear Darcy term only",
            "equation": "deltaP = scenario_multiplier * (300 Pa / 2.84 m/s) * local normal velocity",
            "filter_area_reported_m2": FILTER_AREA_REPORTED_M2,
            "filter_aperture_mesh_m2": FILTER_WIDTH_M * FILTER_HEIGHT_M,
            "length_m": FILTER_DEPTH_M,
            "rho_kg_m3": RHO,
            "nu_m2_s": NU,
            "confirmed_point": {"face_velocity_m_s": CONFIRMED_V_M_S, "initial_delta_P_Pa": CONFIRMED_DP_PA},
            "warning": "APPROXIMATION FROM SINGLE MANUFACTURER DATA POINT",
        },
        "cases": {},
    }

    for case_name, scenario in SCENARIOS.items():
        case = PHASE_ROOT / case_name
        if numeric_solution_directories(case):
            raise RuntimeError(f"Existing solved case protected: {case}")
        case.mkdir(parents=True, exist_ok=True)
        copy_case_physics(case)
        mesh = create_mesh_dictionary(case, boxes)
        darcy_d = LINEAR_SLOPE_PA_PER_M_S * scenario["multiplier"] / (RHO * NU * FILTER_DEPTH_M)
        create_baffles_dictionary(case, darcy_d)
        (case / f"{case_name}.foam").touch()
        implementation = {
            "case": case_name,
            "scenario_classification": "ENGINEERING SENSITIVITY — NOT MEASURED" if case_name != "CASE_M" else "SINGLE-POINT CALIBRATED APPROXIMATION",
            "basis": scenario["basis"],
            "resistance_multiplier": scenario["multiplier"],
            "linear_slope_Pa_per_m_s": LINEAR_SLOPE_PA_PER_M_S * scenario["multiplier"],
            "darcy_D_per_m2": darcy_d,
            "inertial_I_per_m": 0.0,
            "porous_length_m": FILTER_DEPTH_M,
            "filter_active_face_bounds_m": [FILTER_X_M, FILTER_Y0_M, FILTER_Y0_M + FILTER_WIDTH_M, FILTER_Z0_M, FILTER_Z0_M + FILTER_HEIGHT_M],
            "filter_reported_gross_area_m2": FILTER_AREA_REPORTED_M2,
            "mesh_aperture_area_m2": FILTER_WIDTH_M * FILTER_HEIGHT_M,
            "source_filter_sha256": sha256(FILTER_JSON),
            "source_fan_sha256": sha256(FAN_JSON),
            "source_cad_sha256": sha256(SOURCE_CAD),
            "mesh": mesh,
            "fluid_volume_m3": volume,
        }
        (case / "filter_implementation.json").write_text(json.dumps(implementation, indent=2), encoding="utf-8")
        phase_manifest["cases"][case_name] = {
            "resistance_multiplier": scenario["multiplier"],
            "darcy_D_per_m2": darcy_d,
            "total_cells": mesh["total_cells"],
            "block_count": mesh["block_count"],
        }
        print(json.dumps({case_name: phase_manifest["cases"][case_name]}, indent=2))

    (PHASE_ROOT / "filter_case_manifest.json").write_text(json.dumps(phase_manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
