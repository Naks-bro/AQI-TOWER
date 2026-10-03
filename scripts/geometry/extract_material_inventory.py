"""Read existing CAD without saving it; inventory only explicitly listed metal studies."""
import hashlib
import json
from pathlib import Path
import FreeCAD as App

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    'cad/packaging/AQI_Cylindrical_Packaging_R02.FCStd': [
        'Shell', 'HEPAServiceDoor', 'PrefilterServiceDoor',
        'PrefilterBulkhead', 'HEPABulkhead', 'HEPARetainerEnvelope'],
    'cad/packaging/AQI_M04_Airpath_STUDY.FCStd': [
        'Transition', 'InletNeck', 'StraightOutlet'],
}


def extract():
    rows = []
    hashes = {}
    for relative, names in SOURCES.items():
        path = ROOT / relative
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        doc = App.openDocument(str(path))
        try:
            for name in names:
                obj = doc.getObject(name)
                if obj is None or obj.Shape.isNull() or not obj.Shape.isValid():
                    raise RuntimeError('Missing/invalid study part: ' + name)
                shape = obj.Shape
                # Boolean results can be compounds even when they contain one solid.
                solids = shape.Solids
                if not solids or shape.Volume <= 0:
                    raise RuntimeError('No positive solid volume: ' + name)
                centre = sum((s.CenterOfMass*s.Volume for s in solids), App.Vector())/shape.Volume
                rows.append({'source': relative, 'part': name,
                             'volume_mm3': shape.Volume,
                             'geometric_centroid_mm': [centre.x, centre.y, centre.z],
                             'status': 'CAD GEOMETRY; material and structural adequacy UNKNOWN'})
        finally:
            App.closeDocument(doc.Name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != hashes[relative]:
            raise RuntimeError('Source CAD changed during read-only extraction')
    output = ROOT / 'results/fan_selection/material_inventory.json'
    output.write_text(json.dumps({
        'status': 'PARTIAL GEOMETRIC MATERIAL INVENTORY, NOT WHOLE TOWER MASS',
        'source_sha256': hashes, 'parts': rows,
        'excluded': ['FanAllowance', 'HEPAEnvelope', 'PrefilterEnvelope',
                     'HEPAGasketEnvelope', 'ElectricalAllowance', 'BaseAllowance'],
        'missing': ['structural frame/base', 'actual filters', 'guards and louvres',
                    'mounts, hinges, fasteners, seals', 'electrical equipment and cables'],
        'note': 'M04 separate study is not verified as an integrated assembly.'
    }, indent=2) + '\n', encoding='utf-8')
    print('Extracted', len(rows), 'parts; source CAD unchanged:', output)


if __name__ == '__main__':
    extract()
