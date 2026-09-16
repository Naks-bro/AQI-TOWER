"""Independent consistency checks for Phase 8 geometry optimization outputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/GEOMETRY_OPTIMIZATION"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = {}
checks["V00_CAD_preserved_hash"] = sha256(ROOT / "cad/parametric/AQI_Tower_ConceptA_V00.FCStd") == "1bac8a8a7f5bd57b1aa2770b1b02a1653f8fbd21281d9bb256868cf0712424ce"
checks["fan_json_preserved_hash"] = sha256(ROOT / "data/fans/systemair_KVO_250.json") == "847274a70e6d1a56d4707186c6eb37792f96358bb481bad46a704c554de15c73"

metrics = {}
for case in ["GEO_A", "GEO_B", "GEO_C", "GEO_C_CONFIRM"]:
    case_dir = ROOT / "cfd" / case
    audit = json.loads((case_dir / "geometry_audit.json").read_text(encoding="utf-8"))
    metric = json.loads((OUT / case / "metrics.json").read_text(encoding="utf-8"))
    metrics[case] = metric
    checks[f"{case}_CAD_hash_matches_audit"] = sha256(ROOT / audit["source"]) == audit["source_sha256"]
    checks[f"{case}_fan_boundary_matches_V01"] = sha256(case_dir / "0/p") == sha256(ROOT / "cfd/V01_fan/0/p")
    checks[f"{case}_fan_json_matches_V01"] = metric["fan"]["source_json_sha256"] == sha256(ROOT / "data/fans/systemair_KVO_250.json")
    checks[f"{case}_mesh_check_passed"] = "Mesh OK." in (case_dir / "logs/checkMesh.log").read_text(encoding="utf-8")
    checks[f"{case}_mesh_cells_match_audit"] = metric["cell_count"] == audit["total_cells"]
    checks[f"{case}_mesh_resolution_20mm"] = audit["max_cell_edge_mm"] == 20.0
    checks[f"{case}_outlet_area_unchanged"] = abs(audit["boundary_area_m2"]["AIR_OUTLET"] - 0.125) < 1e-12
    checks[f"{case}_mass_criterion"] = metric["criteria"]["mass"]
    checks[f"{case}_flow_stability_criterion"] = metric["criteria"]["flow_stability"]
    checks[f"{case}_fan_closure_criterion"] = metric["criteria"]["fan_closure"]
    checks[f"{case}_inside_fan_curve"] = metric["fan"]["inside_source_curve"]
    checks[f"{case}_empty_stage_declaration"] = audit["stage_treatment"] == "EMPTY FLUID; NO RESISTANCE"

checks["GEO_A_residual_failure_reported"] = not metrics["GEO_A"]["criteria"]["residuals"]
checks["GEO_B_residual_convergence"] = metrics["GEO_B"]["criteria"]["residuals"]
checks["GEO_C_residual_convergence"] = metrics["GEO_C"]["criteria"]["residuals"]
checks["GEO_C_CONFIRM_residual_convergence"] = metrics["GEO_C_CONFIRM"]["criteria"]["residuals"]

confirmation_fields = [
    ("fan", "Q_m3_h"),
    ("fan", "measured_static_equivalent_Pa"),
    ("pressure_Pa", "tower_static_difference"),
    ("pressure_Pa", "tower_flux_weighted_total_loss"),
    ("speed_m_s", "cell_max"),
    ("speed_m_s", "volume_mean"),
    ("regions", "CLEAN_RISER", "reverse_volume_fraction"),
    ("common_riser_window", "reverse_volume_fraction_Uz_below_minus_0p05"),
    ("sections", "riser_entry_above_turn", "normal_velocity_CoV"),
    ("sections", "STAGE_03_mid", "normal_velocity_CoV"),
]


def nested(data, path):
    for key in path:
        data = data[key]
    return data


differences = {
    ".".join(path): nested(metrics["GEO_C_CONFIRM"], path) - nested(metrics["GEO_C"], path)
    for path in confirmation_fields
}
checks["confirmation_key_metrics_exact_match"] = all(value == 0 for value in differences.values())
checks["confirmation_iteration_exact_match"] = metrics["GEO_C_CONFIRM"]["final_iteration"] == metrics["GEO_C"]["final_iteration"] == 926.0
checks["confirmation_mesh_dictionary_exact_match"] = sha256(ROOT / "cfd/GEO_C/system/blockMeshDict") == sha256(ROOT / "cfd/GEO_C_CONFIRM/system/blockMeshDict")
checks["confirmation_solver_dictionary_exact_match"] = sha256(ROOT / "cfd/GEO_C/system/fvSolution") == sha256(ROOT / "cfd/GEO_C_CONFIRM/system/fvSolution")

result = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "confirmation_differences": differences,
    "note": "PASS checks consistency and reproducibility; it is not physical validation or mesh independence.",
}
(OUT / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
if result["status"] != "PASS":
    raise SystemExit(1)
