"""Prepare one fresh GEO_C confirmation case with identical Phase 8 settings."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_phase8_geometry_cases import (  # noqa: E402
    CELL_MM,
    NOTICE,
    ROOT,
    copy_case_physics,
    create_mesh_dictionary,
    numeric_solution_directories,
    read_boxes,
    sha256,
)


def main():
    code = "GEO_C_CONFIRM"
    source = ROOT / "cad/parametric/AQI_Tower_ConceptA_GEO_C.FCStd"
    case = ROOT / "cfd" / code
    if case.exists():
        if numeric_solution_directories(case) or any(case.iterdir()):
            raise RuntimeError(f"Existing confirmation case protected: {case}")
    case.mkdir(parents=True, exist_ok=True)
    boxes, volume = read_boxes(source)
    copy_case_physics(case)
    mesh = create_mesh_dictionary(case, boxes)
    (case / f"{code}.foam").touch()
    audit = {
        "case": code,
        "confirmation_of": "GEO_C",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": sha256(source),
        "units": "CAD millimetres; mesh metres",
        "parameter_notice": NOTICE,
        "regions": boxes,
        "fluid_volume_m3": volume,
        "stage_treatment": "EMPTY FLUID; NO RESISTANCE",
        "fan_model": "Unchanged KVO 250 terminal suction, same orientation and six-point curve",
        "comparison_physics": "Byte-matched GEO_C dictionaries and regenerated identical mesh",
        **mesh,
    }
    (case / "geometry_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    manifest = {
        "case": code,
        "confirmation_of": "GEO_C",
        "source_cad_sha256": audit["source_sha256"],
        "fluid_volume_m3": volume,
        "total_cells": mesh["total_cells"],
        "max_cell_edge_mm": CELL_MM,
        "fan_json_sha256": sha256(ROOT / "data/fans/systemair_KVO_250.json"),
    }
    (case / "confirmation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
