"""Create and validate the AQI Tower Concept A V00 FreeCAD model.

All numerical dimensions in this file are modelling placeholders used only to
produce an editable first geometry. They are not product requirements.
"""

from pathlib import Path

import FreeCAD as App

try:
    import FreeCADGui as Gui

    Gui.showMainWindow()
except (ImportError, AttributeError):
    Gui = None


DOCUMENT_NAME = "AQI_Tower_ConceptA_V00"
OUTPUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "cad"
    / "parametric"
    / "AQI_Tower_ConceptA_V00.FCStd"
)
PREVIEW_PATH = (
    Path(__file__).resolve().parents[2]
    / "reports"
    / "AQI_Tower_ConceptA_V00_preview.png"
)
PLACEHOLDER_NOTICE = "MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT"


PLACEHOLDER_PARAMETERS = [
    ("TowerHeight", "2000 mm", "Overall reference-envelope height"),
    ("TowerWidth", "800 mm", "Overall reference-envelope width"),
    ("TowerDepth", "700 mm", "Overall reference-envelope depth and airflow direction"),
    ("InletHeight", "700 mm", "Height of the inlet and lower airflow path"),
    ("InletWidth", "600 mm", "Width of the inlet and lower airflow path"),
    ("InletBaseZ", "150 mm", "Inlet lower-edge position above the model origin"),
    ("OutletHeight", "250 mm", "Height of the rear outlet region"),
    ("OutletWidth", "500 mm", "Width of the rear outlet and clean-air riser"),
    ("OutletPosition", "1600 mm", "Outlet lower-edge position above the model origin"),
    ("DirtyAirPlenumDepth", "140 mm", "Depth of the dirty-air distribution region"),
    ("TreatmentRegionThickness", "30 mm", "Generic thickness of each treatment placeholder"),
    ("TreatmentRegionSpacing", "40 mm", "Clear airflow spacing between treatment placeholders"),
    ("CleanAirPlenumDepth", "180 mm", "Depth of the lower clean-air collection region"),
    ("InterfaceThickness", "10 mm", "Visual thickness used for inlet and outlet regions"),
]


DERIVED_PARAMETERS = [
    ("AirPathY", "=(B3-B6)/2", "Centers the lower airflow path across the tower width"),
    ("OutletY", "=(B3-B9)/2", "Centers the outlet and riser across the tower width"),
    ("Stage01X", "=B15+B11", "Start of treatment stage 01"),
    ("Stage02X", "=B18+B12+B13", "Start of treatment stage 02"),
    ("Stage03X", "=B19+B12+B13", "Start of treatment stage 03"),
    ("CleanPlenumX", "=B20+B12", "Start of the clean-air collection plenum"),
    ("StageTopZ", "=B7+B5", "Top of lower treatment and collection regions"),
    ("RiserLength", "=B4-B21-B15", "Riser length to the inner outlet boundary"),
    ("RiserHeight", "=B2-B22", "Riser height from treatment top to tower top"),
]


def configure_parameter_sheet(document):
    sheet = document.addObject("Spreadsheet::Sheet", "Parameters")
    sheet.Label = "Parameters — MODELLING PLACEHOLDERS"
    sheet.set("A1", "Parameter")
    sheet.set("B1", "Value")
    sheet.set("C1", "Status")
    sheet.set("D1", "Description")

    for row, (name, value, description) in enumerate(PLACEHOLDER_PARAMETERS, start=2):
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", value)
        sheet.setAlias(f"B{row}", name)
        sheet.set(f"C{row}", PLACEHOLDER_NOTICE)
        sheet.set(f"D{row}", description)

    derived_start = 2 + len(PLACEHOLDER_PARAMETERS)
    for row, (name, formula, description) in enumerate(DERIVED_PARAMETERS, start=derived_start):
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", formula)
        sheet.setAlias(f"B{row}", name)
        sheet.set(f"C{row}", "DERIVED FROM MODELLING PLACEHOLDERS")
        sheet.set(f"D{row}", description)

    sheet.setStyle("A1:D1", "bold", "add")
    sheet.setColumnWidth("A", 190)
    sheet.setColumnWidth("B", 120)
    sheet.setColumnWidth("C", 330)
    sheet.setColumnWidth("D", 440)
    return sheet


def add_metadata(obj, role, cfd_region):
    obj.addProperty("App::PropertyString", "Role", "AQI Tower Metadata")
    obj.addProperty("App::PropertyString", "CFDRegion", "AQI Tower Metadata")
    obj.addProperty("App::PropertyString", "ParameterStatus", "AQI Tower Metadata")
    obj.Role = role
    obj.CFDRegion = cfd_region
    obj.ParameterStatus = PLACEHOLDER_NOTICE


def set_placement_expressions(obj, x=None, y=None, z=None):
    if x:
        obj.setExpression("Placement.Base.x", x)
    if y:
        obj.setExpression("Placement.Base.y", y)
    if z:
        obj.setExpression("Placement.Base.z", z)


def create_box(
    document,
    name,
    label,
    length_expression,
    width_expression,
    height_expression,
    role,
    cfd_region,
    color,
    transparency,
    x=None,
    y=None,
    z=None,
):
    obj = document.addObject("Part::Box", name)
    obj.Label = label
    obj.setExpression("Length", length_expression)
    obj.setExpression("Width", width_expression)
    obj.setExpression("Height", height_expression)
    set_placement_expressions(obj, x=x, y=y, z=z)
    add_metadata(obj, role, cfd_region)
    if obj.ViewObject is not None:
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.LineColor = tuple(max(0.0, component * 0.65) for component in color)
        obj.ViewObject.Transparency = transparency
    return obj


def build_document():
    if DOCUMENT_NAME in App.listDocuments():
        App.closeDocument(DOCUMENT_NAME)

    document = App.newDocument(DOCUMENT_NAME, "AQI Tower Concept A V00")

    parameter_group = document.addObject("App::DocumentObjectGroup", "ParameterDefinitions")
    parameter_group.Label = "00 — Central Parameter Definition"
    reference_group = document.addObject("App::DocumentObjectGroup", "ReferenceGeometry")
    reference_group.Label = "01 — Reference Geometry"
    airflow_group = document.addObject("App::DocumentObjectGroup", "AirflowRegions")
    airflow_group.Label = "02 — Airflow Regions"
    treatment_group = document.addObject("App::DocumentObjectGroup", "TreatmentRegions")
    treatment_group.Label = "03 — Treatment Placeholders"

    sheet = configure_parameter_sheet(document)
    parameter_group.addObject(sheet)

    envelope = create_box(
        document,
        "TowerEnvelope",
        "TowerEnvelope — REFERENCE ONLY",
        "Parameters.TowerDepth",
        "Parameters.TowerWidth",
        "Parameters.TowerHeight",
        "Reference envelope; not a CFD fluid region or final enclosure",
        "REFERENCE_ONLY",
        (0.65, 0.65, 0.70),
        88,
    )
    if envelope.ViewObject is not None:
        envelope.ViewObject.DisplayMode = "Wireframe"
    reference_group.addObject(envelope)

    inlet = create_box(
        document,
        "Inlet",
        "Inlet [AIR_INLET]",
        "Parameters.InterfaceThickness",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Ambient-air inlet interface region",
        "AIR_INLET",
        (0.20, 0.45, 0.95),
        15,
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    airflow_group.addObject(inlet)

    dirty_plenum = create_box(
        document,
        "DirtyAirPlenum",
        "DirtyAirPlenum [DIRTY_PLENUM]",
        "Parameters.DirtyAirPlenumDepth",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Dirty-air distribution volume",
        "DIRTY_PLENUM",
        (0.95, 0.55, 0.18),
        70,
        x="Parameters.InterfaceThickness",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    airflow_group.addObject(dirty_plenum)

    stage_01 = create_box(
        document,
        "TreatmentStage_01",
        "TreatmentStage_01 [STAGE_01]",
        "Parameters.TreatmentRegionThickness",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Generic treatment resistance region; material and function are unassigned",
        "STAGE_01",
        (0.95, 0.82, 0.20),
        38,
        x="Parameters.Stage01X",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    treatment_group.addObject(stage_01)

    gap_01 = create_box(
        document,
        "InterstageGap_01",
        "InterstageGap_01",
        "Parameters.TreatmentRegionSpacing",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Air volume between treatment stages 01 and 02",
        "INTERSTAGE_01",
        (0.78, 0.86, 0.95),
        82,
        x="Parameters.Stage01X + Parameters.TreatmentRegionThickness",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    airflow_group.addObject(gap_01)

    stage_02 = create_box(
        document,
        "TreatmentStage_02",
        "TreatmentStage_02 [STAGE_02]",
        "Parameters.TreatmentRegionThickness",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Generic treatment resistance region; material and function are unassigned",
        "STAGE_02",
        (0.34, 0.75, 0.38),
        38,
        x="Parameters.Stage02X",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    treatment_group.addObject(stage_02)

    gap_02 = create_box(
        document,
        "InterstageGap_02",
        "InterstageGap_02",
        "Parameters.TreatmentRegionSpacing",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Air volume between treatment stages 02 and 03",
        "INTERSTAGE_02",
        (0.78, 0.86, 0.95),
        82,
        x="Parameters.Stage02X + Parameters.TreatmentRegionThickness",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    airflow_group.addObject(gap_02)

    stage_03 = create_box(
        document,
        "TreatmentStage_03",
        "TreatmentStage_03 [STAGE_03]",
        "Parameters.TreatmentRegionThickness",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Generic treatment resistance region; material and function are unassigned",
        "STAGE_03",
        (0.66, 0.40, 0.82),
        38,
        x="Parameters.Stage03X",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    treatment_group.addObject(stage_03)

    clean_plenum = create_box(
        document,
        "CleanAirPlenum",
        "CleanAirPlenum [CLEAN_PLENUM]",
        "Parameters.CleanAirPlenumDepth",
        "Parameters.InletWidth",
        "Parameters.InletHeight",
        "Lower clean-air collection volume",
        "CLEAN_PLENUM",
        (0.18, 0.78, 0.86),
        70,
        x="Parameters.CleanPlenumX",
        y="Parameters.AirPathY",
        z="Parameters.InletBaseZ",
    )
    airflow_group.addObject(clean_plenum)

    riser = create_box(
        document,
        "CleanAirRiser",
        "CleanAirRiser [CLEAN_RISER]",
        "Parameters.RiserLength",
        "Parameters.OutletWidth",
        "Parameters.RiserHeight",
        "Upper clean-air riser and outlet-transition volume",
        "CLEAN_RISER",
        (0.20, 0.82, 0.90),
        76,
        x="Parameters.CleanPlenumX",
        y="Parameters.OutletY",
        z="Parameters.StageTopZ",
    )
    airflow_group.addObject(riser)

    outlet = create_box(
        document,
        "Outlet",
        "Outlet [AIR_OUTLET]",
        "Parameters.InterfaceThickness",
        "Parameters.OutletWidth",
        "Parameters.OutletHeight",
        "Clean-air outlet interface region",
        "AIR_OUTLET",
        (0.12, 0.62, 0.95),
        15,
        x="Parameters.TowerDepth - Parameters.InterfaceThickness",
        y="Parameters.OutletY",
        z="Parameters.OutletPosition",
    )
    airflow_group.addObject(outlet)

    document.recompute()
    return document


def validate_geometry(document):
    sheet = document.getObject("Parameters")
    region_names = [
        "Inlet",
        "DirtyAirPlenum",
        "TreatmentStage_01",
        "InterstageGap_01",
        "TreatmentStage_02",
        "InterstageGap_02",
        "TreatmentStage_03",
        "CleanAirPlenum",
        "CleanAirRiser",
        "Outlet",
    ]

    missing = [name for name in region_names if document.getObject(name) is None]
    if missing:
        raise RuntimeError(f"Missing required regions: {missing}")

    for name in region_names + ["TowerEnvelope"]:
        obj = document.getObject(name)
        if not obj.Shape or obj.Shape.isNull():
            raise RuntimeError(f"{name} has no shape")
        if not obj.Shape.isValid():
            raise RuntimeError(f"{name} has an invalid shape")
        if len(obj.Shape.Solids) != 1:
            raise RuntimeError(f"{name} does not contain exactly one solid")
        problem_states = [state for state in obj.State if state != "Up-to-date"]
        if problem_states:
            raise RuntimeError(f"{name} reports state errors: {problem_states}")

    bounds_seen = {}
    for name in region_names:
        box = document.getObject(name).Shape.BoundBox
        key = tuple(
            round(value, 6)
            for value in (box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax)
        )
        if key in bounds_seen:
            raise RuntimeError(f"Duplicate region bounds: {bounds_seen[key]} and {name}")
        bounds_seen[key] = name

    for index, left_name in enumerate(region_names):
        left_shape = document.getObject(left_name).Shape
        for right_name in region_names[index + 1 :]:
            right_shape = document.getObject(right_name).Shape
            overlap_volume = left_shape.common(right_shape).Volume
            if overlap_volume > 1e-5:
                raise RuntimeError(
                    f"Unexpected volume overlap between {left_name} and {right_name}: "
                    f"{overlap_volume} mm^3"
                )

    connected_pairs = list(zip(region_names[:-1], region_names[1:]))
    for left_name, right_name in connected_pairs:
        distance = document.getObject(left_name).Shape.distToShape(
            document.getObject(right_name).Shape
        )[0]
        if distance > 1e-6:
            raise RuntimeError(
                f"Disconnected airflow regions: {left_name} to {right_name} ({distance} mm)"
            )

    initial_height_text = sheet.getContents("B2")
    initial_spacing_text = sheet.getContents("B13")
    initial_height = document.getObject("TowerEnvelope").Height.Value
    initial_stage_03_x = document.getObject("TreatmentStage_03").Placement.Base.x

    sheet.set("B2", "2050 mm")
    sheet.set("B13", "55 mm")
    document.recompute()

    changed_height = document.getObject("TowerEnvelope").Height.Value
    changed_stage_03_x = document.getObject("TreatmentStage_03").Placement.Base.x
    if abs(changed_height - initial_height) < 1e-6:
        raise RuntimeError("TowerHeight parameter did not regenerate the envelope")
    if abs(changed_stage_03_x - initial_stage_03_x) < 1e-6:
        raise RuntimeError("TreatmentRegionSpacing did not regenerate stage positions")

    sheet.set("B2", initial_height_text)
    sheet.set("B13", initial_spacing_text)
    document.recompute()

    restored_height = document.getObject("TowerEnvelope").Height.Value
    restored_stage_03_x = document.getObject("TreatmentStage_03").Placement.Base.x
    if abs(restored_height - initial_height) > 1e-6:
        raise RuntimeError("TowerHeight did not restore correctly")
    if abs(restored_stage_03_x - initial_stage_03_x) > 1e-6:
        raise RuntimeError("TreatmentRegionSpacing did not restore correctly")

    return {
        "regions": len(region_names),
        "valid_solids": len(region_names) + 1,
        "duplicate_regions": 0,
        "overlapping_airflow_volumes": 0,
        "connected_interfaces": len(connected_pairs),
        "parameter_regeneration": "PASS",
        "restored_placeholder_values": "PASS",
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = build_document()
    validation = validate_geometry(document)
    document.recompute()
    if Gui is not None and Gui.activeDocument() is not None:
        view = Gui.activeDocument().activeView()
        view.viewAxonometric()
        view.fitAll()
        Gui.updateGui()
    document.saveAs(str(OUTPUT_PATH))
    App.closeDocument(document.Name)

    reopened = App.openDocument(str(OUTPUT_PATH))
    reopened.recompute()
    reopen_validation = validate_geometry(reopened)
    reopened.recompute()
    if Gui is not None and Gui.activeDocument() is not None:
        view = Gui.activeDocument().activeView()
        view.viewAxonometric()
        view.fitAll()
        Gui.updateGui()
        view.saveImage(str(PREVIEW_PATH), 1600, 1000, "Current")
    reopened.save()

    print(f"MODEL_PATH={OUTPUT_PATH}")
    print(f"PREVIEW_PATH={PREVIEW_PATH}")
    print(f"DOCUMENT={reopened.Name}")
    print(f"OBJECT_COUNT={len(reopened.Objects)}")
    print(f"BUILD_VALIDATION={validation}")
    print(f"REOPEN_VALIDATION={reopen_validation}")
    print(f"PLACEHOLDER_NOTICE={PLACEHOLDER_NOTICE}")
    App.closeDocument(reopened.Name)


if __name__ == "__main__":
    main()
