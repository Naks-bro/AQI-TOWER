"""Create separate assumed tube routes and check their conflicts with existing CAD."""
import argparse
import hashlib
import json
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]


def build(config_path):
    config = json.loads(config_path.read_text(encoding='utf-8'))
    segmented = config.get('revision') == 'SEGMENTED_R01'
    basename = 'AQI_M02_Segmented_Frame' if segmented else 'AQI_M02_Frame_Routing'
    x, y = config['post_x'], config['post_y']
    a, t = config['profile_outer'], config['profile_wall']
    z0, z1 = config['post_start_z'], config['post_end_z']
    if not (0 < 2*t < a and x > a and y > a and z1 > z0):
        raise ValueError('Invalid route dimensions')
    doc = App.newDocument(basename+'_STUDY')
    parts = []

    def tube(name, length, axis, centre, bottom):
        # Rectangular hollow profiles with open ends; joints have NOT been designed.
        cx, cy = centre
        if axis == 'z':
            outer = Part.makeBox(a, a, length, App.Vector(cx-a/2, cy-a/2, bottom))
            cap = t if config.get('cap_vertical_posts') else 0
            if length <= 2*cap:
                raise ValueError('Post segment too short')
            inner = Part.makeBox(a-2*t, a-2*t, length-2*cap, App.Vector(cx-a/2+t, cy-a/2+t, bottom+cap))
        elif axis == 'x':
            outer = Part.makeBox(length, a, a, App.Vector(-length/2, cy-a/2, bottom))
            inner = Part.makeBox(length, a-2*t, a-2*t, App.Vector(-length/2, cy-a/2+t, bottom+t))
        else:
            outer = Part.makeBox(a, length, a, App.Vector(cx-a/2, -length/2, bottom))
            inner = Part.makeBox(a-2*t, length, a-2*t, App.Vector(cx-a/2+t, -length/2, bottom+t))
        shape = outer.cut(inner)
        if not shape.isValid() or len(shape.Solids) != 1:
            raise RuntimeError('Invalid tube ' + name)
        if axis == 'z':
            expected_volume = a*a*length-(a-2*t)**2*(length-2*cap)
            assert abs(shape.Volume-expected_volume) < 1e-4
        obj = doc.addObject('Part::Feature', name)
        obj.Shape = shape
        obj.addProperty('App::PropertyString', 'EvidenceStatus')
        obj.EvidenceStatus = config['status']
        parts.append(obj)

    for i, (cx, cy) in enumerate([(x,y),(-x,y),(-x,-y),(x,-y)]):
        segments = config.get('post_segments_z', [[z0,z1]])
        for j, (start, end) in enumerate(segments):
            tube('Post'+str(i+1)+(f'Segment{j+1}' if segmented else ''), end-start, 'z', (cx,cy), start)
    for level, top in enumerate(config['rail_top_z']):
        for side in (-1,1):
            tag = 'Neg' if side < 0 else 'Pos'
            tube(f'Rail{level+1}X{tag}', 2*x-a, 'x', (0,side*y), top-a)
            tube(f'Rail{level+1}Y{tag}', 2*y-a, 'y', (side*x,0), top-a)
    doc.recompute()
    conflicts = []
    checked = []
    source_hashes = {}
    assembly_shapes = []
    source_specs = {
        'cad/packaging/AQI_Cylindrical_Packaging_R02.FCStd': [
            'Shell','HEPAServiceDoor','PrefilterServiceDoor','HEPAEnvelope',
            'PrefilterEnvelope','HEPABulkhead','PrefilterBulkhead',
            'HEPAGasketEnvelope','HEPARetainerEnvelope','FanAllowance'],
        'cad/packaging/AQI_M04_Airpath_STUDY.FCStd': ['Transition','InletNeck','StraightOutlet']}
    for relative, names in source_specs.items():
        path = ROOT/relative
        source_hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        source = App.openDocument(str(path))
        try:
            for name in names:
                target = source.getObject(name)
                if target is None:
                    raise RuntimeError('Missing reference ' + name)
                checked.append(name)
                assembly_shapes.append((name, target.Shape.copy()))
                for route in parts:
                    overlap = route.Shape.common(target.Shape).Volume
                    if overlap > 1e-4:
                        conflicts.append({'route': route.Name, 'reference': name,
                                          'overlap_mm3': round(overlap,4)})
        finally:
            App.closeDocument(source.Name)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source_hashes[relative]
    # Reference sweep follows the earlier assumed lifted HEPA extraction, not handling validation.
    sweep = Part.makeBox(593, 1100, 292, App.Vector(-296.5,-803.5,653))
    sweep_clashes = [obj.Name for obj in parts if obj.Shape.common(sweep).Volume > 1e-4]
    internal_clashes = []
    for i, first in enumerate(parts):
        for second in parts[i+1:]:
            if first.Shape.common(second.Shape).Volume > 1e-4:
                internal_clashes.append([first.Name, second.Name])
    folder = ROOT/'cad/packaging'
    fcstd = folder/(basename+'_STUDY.FCStd')
    step = folder/(basename+'_NOT_FOR_FABRICATION.step')
    doc.saveAs(str(fcstd))
    Part.export(parts, str(step))
    imported = Part.read(str(step))
    assert imported.isValid() and len(imported.Solids) == len(parts)
    volume = sum(obj.Shape.Volume for obj in parts)
    audit = {'status':config['status'], 'valid_route_solids':len(parts),
             'STEP_reimport':'PASS','native_reopen':'PENDING',
             'checked_reference_objects':checked, 'nominal_positive_volume_conflicts':conflicts,
             'assumed_HEPA_sweep_conflicts':sweep_clashes,
             'route_internal_positive_volume_conflicts':internal_clashes,
             'route_volume_mm3':volume, 'assumed_steel_density_kg_m3':7850,
             'partial_route_steel_mass_kg':volume*1e-9*7850,
             'xy_envelope_mm':[2*x+a,2*y+a],
             'minimum_filter_side_to_post_clearance_mm':x-a/2-593/2,
             'source_sha256_unchanged':source_hashes,
             'notes':config['notes']}
    if segmented:
        # Record nominal cap-to-plate face contact, NOT load capacity or joint/seal approval.
        contacts = []
        plate_shapes = {name:shape for name,shape in assembly_shapes if name in ('HEPABulkhead','PrefilterBulkhead')}
        for post in parts:
            if not post.Name.startswith('Post'):
                continue
            box = post.Shape.BoundBox
            for z in (box.ZMin,box.ZMax):
                face = Part.makePlane(a,a,App.Vector(box.XMin,box.YMin,z))
                for name, plate in plate_shapes.items():
                    area = face.common(plate).Area
                    if area > 1e-4:
                        contacts.append({'post':post.Name,'plate':name,'z_mm':z,
                                         'nominal_face_contact_mm2':round(area,4)})
        audit['nominal_post_cap_plate_contacts'] = contacts
        assert len(contacts) == 16 and all(abs(c['nominal_face_contact_mm2']-a*a)<1e-4 for c in contacts)
        audit['assembly_check'] = 'NO GEOMETRIC CLASH DOES NOT PROVE STRUCTURE OR SEALS'
        if conflicts or sweep_clashes or internal_clashes:
            raise RuntimeError('Segmented branch has unexpected fit conflicts')
        combined = App.newDocument('AQI_M02_M03_Integrated_Fit_STUDY')
        combined_parts = []
        for name, shape in assembly_shapes+[(p.Name,p.Shape.copy()) for p in parts]:
            obj = combined.addObject('Part::Feature',name)
            obj.Shape = shape
            obj.addProperty('App::PropertyString','EvidenceStatus')
            obj.EvidenceStatus = 'SNAPSHOT FIT STUDY; component envelopes not detailed hardware'
            combined_parts.append(obj)
        combined.recompute()
        combined_path = folder/'AQI_M02_M03_Integrated_Fit_STUDY.FCStd'
        combined.saveAs(str(combined_path))
        assembly_step = folder/'AQI_M02_M03_Integrated_NOT_FOR_FABRICATION.step'
        Part.export(combined_parts,str(assembly_step))
        reimport = Part.read(str(assembly_step))
        assert reimport.isValid() and len(reimport.Solids) == len(combined_parts)
        App.closeDocument(combined.Name)
        combined_reopen = App.openDocument(str(combined_path))
        assert all(o.Shape.isValid() for o in combined_reopen.Objects if hasattr(o,'Shape'))
        App.closeDocument(combined_reopen.Name)
        audit['integrated_snapshot_solids'] = len(combined_parts)
        audit['integrated_native_reopen_and_STEP_reimport'] = 'PASS'
        audit['integrated_exclusions'] = ['base/electrical allowances','guards','exact OEM mounts',
                                          'real joints/fasteners','actual gasket compression']
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(fcstd))
    assert all(o.Shape.isValid() for o in reopened.Objects if hasattr(o,'Shape'))
    App.closeDocument(reopened.Name)
    audit['native_reopen'] = 'PASS'
    audit_name = 'M02_SEGMENTED_FRAME_AUDIT.json' if segmented else 'M02_FRAME_ROUTING_AUDIT.json'
    (folder/audit_name).write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,default=ROOT/'cad/parametric/frame_route_m02.json')
    build(parser.parse_args().config)
