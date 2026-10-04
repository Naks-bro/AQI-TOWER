"""Parametric fit study using installed FreeCAD's bundled Python.

Never overwrites historical CAD. R00 outputs are derived from the versioned JSON.
Service doors/windows are assumed geometry, not manufacturing instructions.
"""
import json
import math
import argparse
from pathlib import Path

import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "cad/parametric/cylindrical_packaging_r00.json"
OUT = ROOT / "cad/packaging"


def build(config_path=CONFIG):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    revision = config["revision"]
    detailed = revision in ("R01", "R02")
    p = {key: item["value"] for key, item in config["parameters"].items()}
    if not all(math.isfinite(v) and v > 0 for v in p.values()):
        raise ValueError("Dimensions must be finite and positive")
    if p["InnerDiameter"] <= max(p["HEPASide"], p["PrefilterSide"], p["FanSide"]) * math.sqrt(2):
        raise ValueError("Square component corners cannot fit circular bore")
    if p["ServiceWidth"] <= p["HEPASide"]:
        raise ValueError("Service opening cannot pass HEPA outer envelope")
    if p["FanZ"] + p["FanHeight"] >= p["TowerHeight"]:
        raise ValueError("Fan placeholder leaves no outlet zone")
    doc = App.newDocument("AQI_Cylindrical_Packaging_" + revision)
    sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
    sheet.Label = "EDITABLE PARAMETERS — ASSUMPTIONS, NOT RELEASED DIMENSIONS"
    for row, (name, entry) in enumerate(config["parameters"].items(), 1):
        sheet.set(f"A{row}", name)
        sheet.set(f"B{row}", str(entry["value"]) + " mm")
        sheet.setAlias(f"B{row}", name)
        sheet.set(f"C{row}", entry["status"])
    sheet.setColumnWidth("A", 190)
    sheet.setColumnWidth("C", 430)
    doc.recompute()

    def expression(obj, property_name, value):
        obj.setExpression(property_name, value)

    def metadata(obj, label, status="ASSUMPTION / NOT FOR FABRICATION"):
        obj.Label = label
        obj.addProperty("App::PropertyString", "EvidenceStatus", "Review")
        obj.EvidenceStatus = status
        return obj

    def cylinder(name, radius, height, z="0 mm"):
        obj = doc.addObject("Part::Cylinder", name)
        expression(obj, "Radius", radius)
        expression(obj, "Height", height)
        expression(obj, "Placement.Base.z", z)
        return obj

    def box(name, length, width, height, x, y, z):
        obj = doc.addObject("Part::Box", name)
        for prop, value in [("Length", length), ("Width", width), ("Height", height),
                            ("Placement.Base.x", x), ("Placement.Base.y", y), ("Placement.Base.z", z)]:
            expression(obj, prop, value)
        return obj

    def cut(name, base, tool):
        obj = doc.addObject("Part::Cut", name)
        obj.Base, obj.Tool = base, tool
        return obj

    outer = cylinder("OuterCylinder", "Parameters.InnerDiameter / 2 + Parameters.WallThickness", "Parameters.TowerHeight - 150 mm", "150 mm")
    inner = cylinder("InnerCylinder", "Parameters.InnerDiameter / 2", "Parameters.TowerHeight - 150 mm", "150 mm")
    wall = cut("UnperforatedWall", outer, inner)
    # Aperture tooling extends through the front (-Y) wall only.
    hepa_window = box("HEPAWindowTool", "Parameters.ServiceWidth", "Parameters.InnerDiameter", "340 mm",
                      "-Parameters.ServiceWidth / 2", "-Parameters.InnerDiameter", "625 mm")
    hepa_open_wall = cut("HEPAOpenWall", wall, hepa_window)
    pre_window = box("PrefilterWindowTool", "Parameters.ServiceWidth", "Parameters.InnerDiameter", "90 mm",
                     "-Parameters.ServiceWidth / 2", "-Parameters.InnerDiameter", "430 mm")
    shell = cut("ServiceShell" if detailed else "Shell", hepa_open_wall, pre_window)
    if detailed:
        tools = []
        for index in range(8):
            tool = box("IntakeTool" + str(index), "100 mm", "Parameters.IntakeWidth", "Parameters.IntakeHeight",
                       "Parameters.InnerDiameter / 2 - 40 mm", "-Parameters.IntakeWidth / 2", "230 mm")
            # Rotate full placement including the radial translation around Z.
            doc.recompute()
            placement = App.Placement(App.Vector(), App.Rotation(App.Vector(0, 0, 1), 45 * index))
            tool.Placement = placement.multiply(tool.Placement)
            # Rotated position must remain linked to changing bore diameter.
            angle = math.radians(45 * index)
            expression(tool, "Placement.Base.x", f"(Parameters.InnerDiameter / 2 - 40 mm) * {math.cos(angle)} + Parameters.IntakeWidth / 2 * {math.sin(angle)}")
            expression(tool, "Placement.Base.y", f"(Parameters.InnerDiameter / 2 - 40 mm) * {math.sin(angle)} - Parameters.IntakeWidth / 2 * {math.cos(angle)}")
            tools.append(tool)
        intake_tools = doc.addObject("Part::MultiFuse", "IntakeTools")
        intake_tools.Shapes = tools
        shell = cut("Shell", shell, intake_tools)
    metadata(shell, "Shell — assumed gauge; intake apertures UNGUARDED" if detailed else "Shell — assumed wall gauge; service openings only; INTAKE UNRESOLVED")
    # Removed curved pieces show door envelopes only, without hinges/gaskets.
    doors = []
    for name, tool in [("HEPAServiceDoor", hepa_window), ("PrefilterServiceDoor", pre_window)]:
        obj = doc.addObject("Part::Common", name)
        obj.Base, obj.Tool = wall, tool
        metadata(obj, name + " — curved envelope, no sealing/hinges")
        doors.append(obj)

    physical = [shell] + doors
    filters = []
    for name, side, depth, z in [("Prefilter", "PrefilterSide", "PrefilterDepth", "PrefilterZ"),
                                ("HEPA", "HEPASide", "HEPADepth", "HEPAZ")]:
        obj = box(name + "Envelope", f"Parameters.{side}", f"Parameters.{side}", f"Parameters.{depth}",
                  f"-Parameters.{side} / 2", f"-Parameters.{side} / 2", f"Parameters.{z}")
        metadata(obj, name + " — candidate OUTER ENVELOPE, no media geometry", "HISTORICAL CANDIDATE; orientation/support unapproved")
        filters.append(obj)
        seat_z = "Parameters.HEPAZ - Parameters.GasketThickness - Parameters.BulkheadThickness" if detailed and name == "HEPA" else f"Parameters.{z} - Parameters.BulkheadThickness"
        opening = "HEPASeatOpening" if detailed and name == "HEPA" else side
        disk = cylinder(name + "BulkheadDisk", "Parameters.InnerDiameter / 2", "Parameters.BulkheadThickness", seat_z)
        aperture = box(name + "ApertureTool", f"Parameters.{opening}", f"Parameters.{opening}", "Parameters.BulkheadThickness",
                       f"-Parameters.{opening} / 2", f"-Parameters.{opening} / 2", seat_z)
        plate = cut(name + "Bulkhead", disk, aperture)
        metadata(plate, name + " full-width bulkhead — gasket/clamp/support detail MISSING")
        physical.extend([obj, plate])
    if detailed:
        def square_ring(name, outer_side, inner_side, depth, z):
            outside = box(name + "Outer", outer_side, outer_side, depth,
                          "-(" + outer_side + ") / 2", "-(" + outer_side + ") / 2", z)
            inside = box(name + "Inner", inner_side, inner_side, depth,
                         "-(" + inner_side + ") / 2", "-(" + inner_side + ") / 2", z)
            ring = cut(name, outside, inside)
            metadata(ring, name + " — illustrative envelope; OEM geometry/loads UNKNOWN")
            return ring
        gasket = square_ring("HEPAGasketEnvelope", "Parameters.GasketOuter", "Parameters.HEPASeatOpening",
                             "Parameters.GasketThickness", "Parameters.HEPAZ - Parameters.GasketThickness")
        retainer = square_ring("HEPARetainerEnvelope", "Parameters.RetainerOuter", "Parameters.HEPASeatOpening",
                               "5 mm", "Parameters.HEPAZ + Parameters.HEPADepth")
        physical.extend([gasket, retainer])
    fan_width = "Parameters.FanWidth" if "FanWidth" in p else "Parameters.FanSide"
    fan = box("FanAllowance", "Parameters.FanSide", fan_width, "Parameters.FanHeight",
              "-Parameters.FanSide / 2", "-(" + fan_width + ") / 2", "Parameters.FanZ")
    metadata(fan, config.get("fan_label", "FAN PLACEHOLDER — NOT OEM GEOMETRY"))
    electrical = box("ElectricalAllowance", "Parameters.ElectricalWidth", "Parameters.ElectricalDepth", "Parameters.ElectricalHeight",
                     "Parameters.InnerDiameter / 2 + Parameters.WallThickness + 20 mm", "-Parameters.ElectricalDepth / 2", "160 mm")
    metadata(electrical, "Electrical side enclosure PLACEHOLDER — no internal layout")
    base = cylinder("BaseAllowance", "Parameters.InnerDiameter / 2 + 50 mm", "150 mm")
    metadata(base, "Base envelope ONLY — not a solid metal specification or structure")
    physical.extend([fan, electrical, base])
    service = box("HEPARemovalSweptVolume", "Parameters.HEPASide", "Parameters.HEPASide + Parameters.InnerDiameter / 2 + 300 mm",
                  "Parameters.HEPADepth", "-Parameters.HEPASide / 2",
                  "-Parameters.HEPASide / 2 - Parameters.InnerDiameter / 2 - 300 mm",
                  "Parameters.HEPAZ + Parameters.ServiceLift" if detailed else "Parameters.HEPAZ")
    metadata(service, "REFERENCE: HEPA slide-out swept space — includes installed position, not a part")
    doc.recompute()

    for obj in doc.Objects:
        if hasattr(obj, "Shape") and (obj.Shape.isNull() or not obj.Shape.isValid()):
            raise RuntimeError("Invalid CAD geometry: " + obj.Name)
    clashes = []
    for i, first in enumerate(physical):
        for second in physical[i + 1:]:
            overlap = first.Shape.common(second.Shape).Volume
            if overlap > 1e-4:
                clashes.append({"first": first.Name, "second": second.Name, "overlap_mm3": round(overlap, 4)})
    if clashes:
        raise RuntimeError("Unexpected envelope interference: " + json.dumps(clashes))
    service_overlap = service.Shape.common(shell.Shape).Volume
    if service_overlap > 1e-4:
        raise RuntimeError("Assumed HEPA removal path crosses shell")
    if detailed:
        assert service.Shape.common(gasket.Shape).Volume < 1e-4
        assert service.Shape.common(doc.HEPABulkhead.Shape).Volume < 1e-4
        if p["GasketOuter"] > p["HEPASide"] or p["HEPASeatOpening"] >= p["GasketOuter"]:
            raise ValueError("Gasket ring does not lie under assumed filter frame")
    # Validate expression propagation, then return original dimensions before saving.
    original_x = shell.Shape.BoundBox.XLength
    diameter_row = list(config["parameters"]).index("InnerDiameter") + 1
    sheet.set(f"B{diameter_row}", str(p["InnerDiameter"] + 20) + " mm")
    doc.recompute()
    if abs(shell.Shape.BoundBox.XLength - original_x - 20) > 1e-5:
        raise RuntimeError("Parameter update did not propagate into shell")
    sheet.set(f"B{diameter_row}", str(p["InnerDiameter"]) + " mm")
    doc.recompute()
    OUT.mkdir(parents=True, exist_ok=True)
    fcstd = OUT / f"AQI_Cylindrical_Packaging_{revision}.FCStd"
    step = OUT / f"AQI_Cylindrical_Packaging_{revision}_NOT_FOR_FABRICATION.step"
    doc.saveAs(str(fcstd))
    Part.export(physical, str(step))
    exchange = Part.read(str(step))
    if not exchange.isValid() or len(exchange.Solids) != len(physical):
        raise RuntimeError("STEP reimport invalid or solid count mismatch")
    audit = {
        "status": config["status"], "FreeCAD_version": App.Version(), "source": str(config_path.relative_to(ROOT)),
        "objects_exported": [obj.Name for obj in physical],
        "square_HEPA_diagonal_mm": round(p["HEPASide"] * math.sqrt(2), 3),
        "radial_corner_clearance_mm": round((p["InnerDiameter"] - p["HEPASide"] * math.sqrt(2)) / 2, 3),
        "solid_validity": "PASS for generated geometry", "unexpected_overlaps": clashes,
        "HEPA_assumed_removal_sweep_shell_overlap_mm3": round(service_overlap, 6),
        "parametric_diameter_propagation": "PASS: +20mm check, restored before save",
        "STEP_reimport_valid_solids": len(exchange.Solids),
        "limits": config["excluded"] + (["Intake apertures unguarded; no released airflow assembly"] if detailed else ["Intake openings not cut: shell is NOT a working air path"]) + [
                    "No OEM fan envelope fit established", "No gasket compression or realistic filter support designed",
                    "No structural analysis, service hardware clearance or pressure prediction"],
    }
    if detailed:
        audit["service_sequence"] = "Isolate, remove retainer, lift filter 5mm assumption, slide out using rated handling system; not designed"
        audit["intake_projected_open_area_m2"] = 8 * p["IntakeWidth"] * p["IntakeHeight"] / 1e6
        audit["intake_geometric_void_volume_mm3"] = doc.ServiceShell.Shape.Volume - shell.Shape.Volume
        audit["effective_HEPA_clear_opening_m2_ASSUMED"] = (p["HEPASeatOpening"] / 1000) ** 2
    (OUT / f"PACKAGING_{revision}_AUDIT.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    App.closeDocument(doc.Name)
    loaded = App.openDocument(str(fcstd))
    loaded.recompute()
    assert loaded.HEPAEnvelope.Shape.isValid()
    assert abs(loaded.HEPAEnvelope.Shape.BoundBox.ZLength - p["HEPADepth"]) < 1e-6
    App.closeDocument(loaded.Name)
    print(json.dumps(audit, indent=2))
    print("Saved and reopened:", fcstd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    build(parser.parse_args().config.resolve())
