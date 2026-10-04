"""Read assumed steel material above each plate; never assign placeholder masses."""
import hashlib
import json
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]


def extract():
    specs = {
        'cad/packaging/AQI_M02_Segmented_Frame_STUDY.FCStd': None,
        'cad/packaging/AQI_M04_Airpath_STUDY.FCStd': ['Transition','InletNeck','StraightOutlet'],
        'cad/packaging/AQI_Cylindrical_Packaging_R02.FCStd': ['HEPABulkhead','HEPARetainerEnvelope'],
    }
    rows, hashes = [], {}
    for relative, selected in specs.items():
        path = ROOT/relative
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        doc = App.openDocument(str(path))
        try:
            objects = [o for o in doc.Objects if hasattr(o,'Shape')] if selected is None else [doc.getObject(n) for n in selected]
            for obj in objects:
                if obj is None or not obj.Shape.isValid():
                    raise RuntimeError('Missing/invalid reference part')
                for boundary, z in [('HEPA_upper_face',645),('prefilter_upper_face',450)]:
                    clip = Part.makeBox(4000,4000,5000,App.Vector(-2000,-2000,z))
                    volume = obj.Shape.common(clip).Volume
                    if volume > 1e-4:
                        rows.append({'boundary':boundary,'part':obj.Name,'source':relative,
                                     'volume_above_mm3':volume,
                                     'mass_kg_at_ASSUMED_steel_7850':volume*1e-9*7850})
        finally:
            App.closeDocument(doc.Name)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == hashes[relative]
    totals = {name:sum(r['mass_kg_at_ASSUMED_steel_7850'] for r in rows if r['boundary']==name)
              for name in ('HEPA_upper_face','prefilter_upper_face')}
    output = {'status':'PARTIAL MATERIAL ABOVE PLANE, NOT ACTUAL SUPPORT LOAD',
              'source_sha256_unchanged':hashes,'plane_material_totals_kg_ASSUMED_steel':totals,
              'parts':rows,'fan_candidate_OEM_mass_kg':14,
              'excluded':['shell/doors (attachment load path unknown)','actual filter masses',
                          'gasket, mounts, joints, guards, wiring and electronics',
                          'base, floor and any ballast'],
              'notes':['Homogeneous steel and route through posts are scenario assumptions',
                       'Fan 14 kg is separate from material totals and remains unselected',
                       'Clip above upper face excludes that boundary plate itself',
                       'Loads above successive planes are NOT additive machine masses']}
    target = ROOT/'results/fan_selection/support_load_inventory.json'
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(totals,indent=2))


if __name__ == '__main__':
    extract()
