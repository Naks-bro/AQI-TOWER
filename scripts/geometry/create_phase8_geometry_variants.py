"""Create the three Phase 8 parametric FreeCAD airflow-geometry trials.

All dimensions are design experiment parameters, not product requirements.
The script creates new files only and never opens V00 for writing.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "cad" / "parametric"
AUDIT_PATH = OUT_DIR / "PHASE8_GEOMETRY_AUDIT.json"
NOTICE = "DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT"

VARIANTS = {
    "GEO_A": {
        "filename": "AQI_Tower_ConceptA_GEO_A.FCStd",
        "riser_inner_x_mm": 320.0,
        "riser_top_z_mm": 2000.0,
        "turn_steps": True,
        "intent": "Two-step outer turning chamber; original riser width and blind cap retained.",
    },
    "GEO_B": {
        "filename": "AQI_Tower_ConceptA_GEO_B.FCStd",
        "riser_inner_x_mm": 260.0,
        "riser_top_z_mm": 2000.0,
        "turn_steps": False,
        "intent": "Riser inner wall shifted upstream by 60 mm; no outer turning chamber.",
    },
    "GEO_C": {
        "filename": "AQI_Tower_ConceptA_GEO_C.FCStd",
        "riser_inner_x_mm": 260.0,
        "riser_top_z_mm": 1850.0,
        "turn_steps": True,
        "intent": "Combined enlarged entry and two-step turn; blind cap above outlet removed.",
    },
}

COMMON_PARAMETERS = [
    ("TowerHeight", "2000 mm", "Reference-envelope height"),
    ("TowerWidth", "800 mm", "Reference-envelope width"),
    ("TowerDepth", "700 mm", "Reference-envelope depth / lower flow direction"),
    ("InletHeight", "700 mm", "Lower airflow-path height"),
    ("InletWidth", "600 mm", "Lower airflow-path width"),
    ("InletBaseZ", "150 mm", "Lower airflow-path base elevation"),
    ("OutletHeight", "250 mm", "Side outlet height"),
    ("OutletWidth", "500 mm", "Side outlet width"),
    ("OutletPosition", "1600 mm", "Side outlet base elevation"),
    ("DirtyAirPlenumDepth", "140 mm", "Dirty plenum depth"),
    ("TreatmentRegionThickness", "30 mm", "Empty stage-zone thickness"),
    ("TreatmentRegionSpacing", "40 mm", "Empty interstage spacing"),
    ("CleanAirPlenumDepth", "180 mm", "Original lower clean-plenum depth"),
    ("InterfaceThickness", "10 mm", "Inlet and outlet interface length"),
    ("TurnStep01StartX", "500 mm", "First outer turning-chamber step start"),
    ("TurnStep01Length", "90 mm", "First outer turning-chamber step length"),
    ("TurnStep01BaseZ", "450 mm", "First outer turning-chamber step base"),
    ("TurnStep02StartX", "590 mm", "Second outer turning-chamber step start"),
    ("TurnStep02Length", "100 mm", "Second outer turning-chamber step length"),
    ("TurnStep02BaseZ", "650 mm", "Second outer turning-chamber step base"),
]


def configure_sheet(document, code, spec):
    sheet = document.addObject("Spreadsheet::Sheet", "Parameters")
    sheet.Label = f"{code} Parameters — {NOTICE}"
    for cell, value in [("A1", "Parameter"), ("B1", "Value"), ("C1", "Status"), ("D1", "Description")]:
        sheet.set(cell, value)
    primary = list(COMMON_PARAMETERS) + [
        ("RiserInnerX", f"{spec['riser_inner_x_mm']:.0f} mm", "Inner X wall of clean riser"),
        ("RiserTopZ", f"{spec['riser_top_z_mm']:.0f} mm", "Top of clean-riser fluid region"),
    ]
    rows = {}
    for row, (name, value, description) in enumerate(primary, start=2):
        rows[name] = row
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", value)
        sheet.setAlias(f"B{row}", name)
        sheet.set(f"C{row}", NOTICE)
        sheet.set(f"D{row}", description)
    derived = [
        ("AirPathY", "=(B3-B6)/2", "Centres lower airflow path"),
        ("OutletY", "=(B3-B9)/2", "Centres outlet and riser"),
        ("Stage01X", "=B15+B11", "Stage 01 start"),
        ("Stage02X", f"=B{4 + len(primary)}+B12+B13", "Stage 02 start"),
        ("Stage03X", f"=B{5 + len(primary)}+B12+B13", "Stage 03 start"),
        ("CleanPlenumX", f"=B{6 + len(primary)}+B12", "Clean plenum start"),
        ("StageTopZ", "=B7+B5", "Top of lower airflow path"),
        ("RiserOuterX", "=B4-B15", "Inner boundary of outlet interface"),
        ("RiserLength", f"=B{9 + len(primary)}-B{rows['RiserInnerX']}", "Riser X length"),
        ("RiserHeight", f"=B{rows['RiserTopZ']}-B{8 + len(primary)}", "Riser Z height"),
        ("TurnStep01Height", f"=B{8 + len(primary)}-B{rows['TurnStep01BaseZ']}", "First turn-step height"),
        ("TurnStep02Height", f"=B{8 + len(primary)}-B{rows['TurnStep02BaseZ']}", "Second turn-step height"),
    ]
    for row, (name, formula, description) in enumerate(derived, start=2 + len(primary)):
        rows[name] = row
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", formula)
        sheet.setAlias(f"B{row}", name)
        sheet.set(f"C{row}", f"DERIVED FROM {NOTICE}")
        sheet.set(f"D{row}", description)
    sheet.set("F1", "Variant")
    sheet.set("G1", code)
    sheet.set("F2", "Intent")
    sheet.set("G2", spec["intent"])
    sheet.setStyle("A1:D1", "bold", "add")
    sheet.setStyle("F1:G2", "bold", "add")
    sheet.setColumnWidth("A", 180)
    sheet.setColumnWidth("B", 110)
    sheet.setColumnWidth("C", 360)
    sheet.setColumnWidth("D", 410)
    sheet.setColumnWidth("F", 90)
    sheet.setColumnWidth("G", 520)
    return sheet, rows


def add_metadata(obj, region, role, code):
    obj.addProperty("App::PropertyString", "CFDRegion", "AQI Tower Metadata")
    obj.addProperty("App::PropertyString", "Role", "AQI Tower Metadata")
    obj.addProperty("App::PropertyString", "Variant", "AQI Tower Metadata")
    obj.addProperty("App::PropertyString", "ParameterStatus", "AQI Tower Metadata")
    obj.CFDRegion = region
    obj.Role = role
    obj.Variant = code
    obj.ParameterStatus = NOTICE


def create_box(document, code, group, name, label, region, role, expressions, color, transparency):
    obj = document.addObject("Part::Box", name)
    obj.Label = label
    for prop, expression in expressions.items():
        obj.setExpression(prop, expression)
    add_metadata(obj, region, role, code)
    group.addObject(obj)
    if obj.ViewObject is not None:
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.LineColor = tuple(component * 0.60 for component in color)
        obj.ViewObject.Transparency = transparency
    return obj


def build_document(code, spec):
    document_name = f"AQI_Tower_ConceptA_{code}"
    if document_name in App.listDocuments():
        App.closeDocument(document_name)
    doc = App.newDocument(document_name, f"AQI Tower Concept A {code}")
    parameters = doc.addObject("App::DocumentObjectGroup", "ParameterDefinitions")
    parameters.Label = "00 — Design Experiment Parameters"
    reference = doc.addObject("App::DocumentObjectGroup", "ReferenceGeometry")
    reference.Label = "01 — Reference Geometry"
    airflow = doc.addObject("App::DocumentObjectGroup", "AirflowRegions")
    airflow.Label = "02 — Empty Airflow Regions"
    stages = doc.addObject("App::DocumentObjectGroup", "TreatmentRegions")
    stages.Label = "03 — Empty Stage Regions"
    sheet, rows = configure_sheet(doc, code, spec)
    parameters.addObject(sheet)
    notes = doc.addObject("App::FeaturePython", "Phase8DesignNotes")
    notes.Label = f"{code} — DESIGN EXPERIMENT ONLY"
    notes.addProperty("App::PropertyString", "Status", "Phase 8")
    notes.addProperty("App::PropertyString", "Intent", "Phase 8")
    notes.addProperty("App::PropertyString", "PhysicsBoundary", "Phase 8")
    notes.Status = NOTICE
    notes.Intent = spec["intent"]
    notes.PhysicsBoundary = "EMPTY AIR ONLY; NO FILTER, WATER, PARTICLE OR SOLAR MODEL"
    parameters.addObject(notes)

    envelope = create_box(doc, code, reference, "TowerEnvelope", "TowerEnvelope — REFERENCE ONLY", "REFERENCE_ONLY", "Reference envelope; not fluid or final enclosure", {
        "Length": "Parameters.TowerDepth", "Width": "Parameters.TowerWidth", "Height": "Parameters.TowerHeight"
    }, (0.65, 0.65, 0.70), 90)
    if envelope.ViewObject is not None:
        envelope.ViewObject.DisplayMode = "Wireframe"

    definitions = [
        (airflow, "Inlet", "Inlet [AIR_INLET]", "AIR_INLET", "Ambient inlet interface", {
            "Length": "Parameters.InterfaceThickness", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.20, 0.45, 0.95), 15),
        (airflow, "DirtyAirPlenum", "DirtyAirPlenum [DIRTY_PLENUM]", "DIRTY_PLENUM", "Empty dirty-air plenum", {
            "Length": "Parameters.DirtyAirPlenumDepth", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.InterfaceThickness", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.95, 0.55, 0.18), 72),
        (stages, "TreatmentStage_01", "TreatmentStage_01 [STAGE_01 — EMPTY]", "STAGE_01", "Empty labelled stage volume; no resistance", {
            "Length": "Parameters.TreatmentRegionThickness", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.Stage01X", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.95, 0.82, 0.20), 42),
        (airflow, "InterstageGap_01", "InterstageGap_01", "INTERSTAGE_01", "Empty interstage airflow", {
            "Length": "Parameters.TreatmentRegionSpacing", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.Stage01X+Parameters.TreatmentRegionThickness", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.78, 0.86, 0.95), 84),
        (stages, "TreatmentStage_02", "TreatmentStage_02 [STAGE_02 — EMPTY]", "STAGE_02", "Empty labelled stage volume; no resistance", {
            "Length": "Parameters.TreatmentRegionThickness", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.Stage02X", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.34, 0.75, 0.38), 42),
        (airflow, "InterstageGap_02", "InterstageGap_02", "INTERSTAGE_02", "Empty interstage airflow", {
            "Length": "Parameters.TreatmentRegionSpacing", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.Stage02X+Parameters.TreatmentRegionThickness", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.78, 0.86, 0.95), 84),
        (stages, "TreatmentStage_03", "TreatmentStage_03 [STAGE_03 — EMPTY]", "STAGE_03", "Empty labelled stage volume; no resistance", {
            "Length": "Parameters.TreatmentRegionThickness", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.Stage03X", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.66, 0.40, 0.82), 42),
        (airflow, "CleanAirPlenum", "CleanAirPlenum [CLEAN_PLENUM]", "CLEAN_PLENUM", "Original empty collection plenum", {
            "Length": "Parameters.CleanAirPlenumDepth", "Width": "Parameters.InletWidth", "Height": "Parameters.InletHeight",
            "Placement.Base.x": "Parameters.CleanPlenumX", "Placement.Base.y": "Parameters.AirPathY", "Placement.Base.z": "Parameters.InletBaseZ"}, (0.18, 0.78, 0.86), 72),
        (airflow, "CleanAirRiser", "CleanAirRiser [CLEAN_RISER]", "CLEAN_RISER", "Modified empty riser", {
            "Length": "Parameters.RiserLength", "Width": "Parameters.OutletWidth", "Height": "Parameters.RiserHeight",
            "Placement.Base.x": "Parameters.RiserInnerX", "Placement.Base.y": "Parameters.OutletY", "Placement.Base.z": "Parameters.StageTopZ"}, (0.20, 0.82, 0.90), 76),
        (airflow, "Outlet", "Outlet [AIR_OUTLET]", "AIR_OUTLET", "Unchanged KVO terminal-suction interface", {
            "Length": "Parameters.InterfaceThickness", "Width": "Parameters.OutletWidth", "Height": "Parameters.OutletHeight",
            "Placement.Base.x": "Parameters.RiserOuterX", "Placement.Base.y": "Parameters.OutletY", "Placement.Base.z": "Parameters.OutletPosition"}, (0.12, 0.62, 0.95), 15),
    ]
    objects = []
    for definition in definitions:
        objects.append(create_box(doc, code, *definition))
    if spec["turn_steps"]:
        objects.extend([
            create_box(doc, code, airflow, "TurnStep_01", "TurnStep_01 [TURN_STEP_01]", "TURN_STEP_01", "First empty outer turning-chamber segment", {
                "Length": "Parameters.TurnStep01Length", "Width": "Parameters.OutletWidth", "Height": "Parameters.TurnStep01Height",
                "Placement.Base.x": "Parameters.TurnStep01StartX", "Placement.Base.y": "Parameters.OutletY", "Placement.Base.z": "Parameters.TurnStep01BaseZ"}, (0.38, 0.70, 0.92), 68),
            create_box(doc, code, airflow, "TurnStep_02", "TurnStep_02 [TURN_STEP_02]", "TURN_STEP_02", "Second empty outer turning-chamber segment", {
                "Length": "Parameters.TurnStep02Length", "Width": "Parameters.OutletWidth", "Height": "Parameters.TurnStep02Height",
                "Placement.Base.x": "Parameters.TurnStep02StartX", "Placement.Base.y": "Parameters.OutletY", "Placement.Base.z": "Parameters.TurnStep02BaseZ"}, (0.30, 0.62, 0.90), 68),
        ])
    doc.recompute()
    return doc, sheet, rows, objects


def validate(doc, sheet, rows, objects, spec, exercise_parameters=True):
    for obj in objects + [doc.getObject("TowerEnvelope")]:
        if obj is None or obj.Shape.isNull() or not obj.Shape.isValid() or len(obj.Shape.Solids) != 1:
            raise RuntimeError(f"Invalid single solid: {getattr(obj, 'Name', 'missing')}")
        if [state for state in obj.State if state != "Up-to-date"]:
            raise RuntimeError(f"Object state error: {obj.Name}: {obj.State}")
    for index, left in enumerate(objects):
        for right in objects[index + 1:]:
            if left.Shape.common(right.Shape).Volume > 1e-3:
                raise RuntimeError(f"Overlapping fluid regions: {left.Name}, {right.Name}")
    fused = objects[0].Shape.multiFuse([obj.Shape for obj in objects[1:]]).removeSplitter()
    if not fused.isValid() or len(fused.Solids) != 1:
        raise RuntimeError("Fluid domain does not fuse to one connected solid")
    if abs(fused.Volume - sum(obj.Shape.Volume for obj in objects)) > 1e-3:
        raise RuntimeError("Unexpected duplicate fluid volume")
    initial_x = doc.getObject("CleanAirRiser").Placement.Base.x
    initial_length = doc.getObject("CleanAirRiser").Length.Value
    if exercise_parameters:
        inner_row = rows["RiserInnerX"]
        initial_text = sheet.getContents(f"B{inner_row}")
        sheet.set(f"B{inner_row}", f"{spec['riser_inner_x_mm'] + 10:.0f} mm")
        doc.recompute()
        if abs(doc.getObject("CleanAirRiser").Placement.Base.x - initial_x) < 1e-6:
            raise RuntimeError("RiserInnerX did not regenerate placement")
        if abs(doc.getObject("CleanAirRiser").Length.Value - initial_length) < 1e-6:
            raise RuntimeError("RiserInnerX did not regenerate length")
        sheet.set(f"B{inner_row}", initial_text)
        doc.recompute()
        if abs(doc.getObject("CleanAirRiser").Placement.Base.x - initial_x) > 1e-6:
            raise RuntimeError("RiserInnerX did not restore")
    return {
        "fluid_region_count": len(objects),
        "fused_solid_count": len(fused.Solids),
        "fluid_volume_m3": fused.Volume * 1e-9,
        "parameter_regeneration": "PASS" if exercise_parameters else "NOT REPEATED",
        "validity": "PASS",
        "notice": NOTICE,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    audit = {"phase": 8, "notice": NOTICE, "variants": {}}
    for code, spec in VARIANTS.items():
        path = OUT_DIR / spec["filename"]
        doc, sheet, rows, objects = build_document(code, spec)
        build_check = validate(doc, sheet, rows, objects, spec)
        doc.recompute()
        doc.saveAs(str(path))
        App.closeDocument(doc.Name)

        reopened = App.openDocument(str(path))
        reopened.recompute()
        reopened_objects = [obj for obj in reopened.Objects if getattr(obj, "CFDRegion", "") not in ("", "REFERENCE_ONLY")]
        reopen_check = validate(reopened, reopened.getObject("Parameters"), rows, reopened_objects, spec)
        reopened.recompute()
        reopened.save()
        App.closeDocument(reopened.Name)
        audit["variants"][code] = {
            "file": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "intent": spec["intent"],
            "parameters": {
                "riser_inner_x_mm": spec["riser_inner_x_mm"],
                "riser_top_z_mm": spec["riser_top_z_mm"],
                "turn_steps": spec["turn_steps"],
                "turn_step_01": {"x_mm": [500, 590], "z_mm": [450, 850], "y_mm": [150, 650]} if spec["turn_steps"] else None,
                "turn_step_02": {"x_mm": [590, 690], "z_mm": [650, 850], "y_mm": [150, 650]} if spec["turn_steps"] else None,
            },
            "build_validation": build_check,
            "reopen_validation": reopen_check,
        }
        print(f"{code}: {path} — PASS")
    AUDIT_PATH.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"AUDIT: {AUDIT_PATH}")


if __name__ == "__main__":
    main()
