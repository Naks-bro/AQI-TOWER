"""Continuous surrounding frame + separate inner housing; source CAD stays untouched."""
import hashlib
import json
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]


def build():
    c = json.loads((ROOT/'cad/parametric/independent_housing_m03.json').read_text(encoding='utf-8'))
    side, wall = c['housing_outer_side'], c['housing_wall']
    inner = side-2*wall
    doc = App.newDocument('AQI_M03_Independent_Housing_STUDY')
    objects, hashes = [], {}
    def add(name,shape,kind):
        if shape.isNull() or not shape.isValid() or len(shape.Solids)!=1:
            raise RuntimeError('Invalid study solid: '+name)
        o = doc.addObject('Part::Feature',name)
        o.Shape = shape
        o.addProperty('App::PropertyString','EvidenceStatus')
        o.EvidenceStatus = c['status']
        o.addProperty('App::PropertyString','StudyKind')
        o.StudyKind = kind
        objects.append(o)
        return o
    references = {
        'cad/packaging/AQI_Cylindrical_Packaging_R02.FCStd': [
            'Shell','HEPAServiceDoor','PrefilterServiceDoor','HEPAEnvelope',
            'PrefilterEnvelope','HEPAGasketEnvelope','HEPARetainerEnvelope','FanAllowance'],
        'cad/packaging/AQI_M04_Airpath_STUDY.FCStd': ['Transition','InletNeck','StraightOutlet'],
        'cad/packaging/AQI_M02_Frame_Routing_STUDY.FCStd': None}
    omit = {'Rail2XNeg','Rail2XPos','Rail3XNeg','Rail3XPos'}
    for relative,names in references.items():
        path = ROOT/relative
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        source = App.openDocument(str(path))
        try:
            names = names or [o.Name for o in source.Objects if hasattr(o,'Shape') and o.Name not in omit]
            for name in names:
                obj = source.getObject(name)
                kind = 'envelope' if name in ('FanAllowance','HEPAEnvelope','PrefilterEnvelope','HEPAGasketEnvelope') else 'assumed_material'
                add(name,obj.Shape.copy(),kind)
        finally:
            App.closeDocument(source.Name)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==hashes[relative]

    def square_box(width,height,z):
        return Part.makeBox(width,width,height,App.Vector(-width/2,-width/2,z))

    def housing(z,height):
        return square_box(side,height,z).cut(square_box(inner,height,z))

    def seat(name,opening,z):
        shape = square_box(side,c['seat_thickness'],z).cut(square_box(opening,c['seat_thickness'],z))
        for sx in (-1,1):
            for cy in c['bearing_ear_centres_y']:
                start = side/2-wall
                length = c['bearing_ear_outer_x']-start
                x = start if sx>0 else -c['bearing_ear_outer_x']
                ear = Part.makeBox(length,c['bearing_ear_width'],c['seat_thickness'],
                                   App.Vector(x,cy-c['bearing_ear_width']/2,z))
                shape = shape.fuse(ear)
        return add(name,shape.removeSplitter(),'assumed_material')

    # Eight projected openings, two per inner housing face. Annular approach losses unknown.
    lower = housing(202,243)
    for face in range(4):
        for centre in (-160,160):
            tool = Part.makeBox(160,10,140,App.Vector(centre-80,-side/2-4,230))
            tool.rotate(App.Vector(),App.Vector(0,0,1),face*90)
            lower = lower.cut(tool)
    add('LowerIntakeHousing',lower,'assumed_material')
    pre_seat = seat('IndependentPrefilterSeat',c['prefilter_opening'],445)
    hepa_seat = seat('IndependentHEPASeat',c['HEPA_opening'],640)
    for name,z,height,window_z,window_height in [
        ('DirtyHousing',450,190,453,65),('CleanHousing',645,318,650,310)]:
        shell = housing(z,height)
        tool = Part.makeBox(c['service_opening_width'],10,window_height,
                            App.Vector(-c['service_opening_width']/2,-side/2-4,window_z))
        add(name,shell.cut(tool),'assumed_material')
        add(name+'ServicePanel',shell.common(tool),'assumed_material')
    add('HousingBottom',square_box(side,2,200),'assumed_material')
    add('HousingTopAdapterSeat',square_box(side,2,963).cut(square_box(563,2,963)),'assumed_material')
    doc.recompute()
    conflicts = []
    for i,first in enumerate(objects):
        for second in objects[i+1:]:
            overlap = first.Shape.common(second.Shape).Volume
            if overlap>1e-4:
                conflicts.append({'first':first.Name,'second':second.Name,'volume_mm3':round(overlap,4)})
    sweeps = {
        'HEPA_lifted':Part.makeBox(593,1100,292,App.Vector(-296.5,-803.5,653)),
        'prefilter_lifted':Part.makeBox(592,1100,48,App.Vector(-296,-804,455)),
        'retainer_after_removal_of_clamps':Part.makeBox(633,1100,5,App.Vector(-316.5,-783.5,940))}
    ignore = {'HEPAEnvelope','PrefilterEnvelope','HEPARetainerEnvelope','HEPAServiceDoor',
              'PrefilterServiceDoor','DirtyHousingServicePanel','CleanHousingServicePanel'}
    sweep_clashes = {name:[o.Name for o in objects if o.Name not in ignore and o.Shape.common(shape).Volume>1e-4]
                    for name,shape in sweeps.items()}
    contacts = []
    for seat_o in (pre_seat,hepa_seat):
        for rail in objects:
            if rail.Name.startswith(('Rail2Y','Rail3Y')):
                box = rail.Shape.BoundBox
                for cy in c['bearing_ear_centres_y']:
                    face = Part.makePlane(35,c['bearing_ear_width'],
                                          App.Vector(box.XMin,cy-c['bearing_ear_width']/2,box.ZMax))
                    area = face.common(seat_o.Shape).common(rail.Shape).Area
                    if area>1e-4:
                        contacts.append({'seat':seat_o.Name,'rail':rail.Name,
                                         'ear_y_mm':cy,'nominal_contact_mm2':round(area,4)})
    volume = sum(o.Shape.Volume for o in objects if o.StudyKind=='assumed_material')
    audit = {'status':c['status'],'valid_solids':len(objects),'positive_volume_clashes':conflicts,
             'assumed_service_sweep_clashes_panels_removed':sweep_clashes,
             'nominal_seat_to_side_rail_contacts':contacts,
             'housing_to_post_gap_mm':350-35/2-side/2,
             'retainer_to_inner_service_opening_side_margin_mm':(c['service_opening_width']-633)/2,
             'inner_housing_intake_gross_area_m2':8*.160*.140,
             'partial_all_assumed_material_steel_mass_kg':volume*1e-9*7850,
             'mass_excludes':['fan, filters, gasket, base, all real hardware/electrics'],
             'omitted_old_parts':['HEPABulkhead','PrefilterBulkhead']+sorted(omit),
             'source_sha256_unchanged':hashes,'notes':c['notes']}
    if conflicts or any(sweep_clashes.values()) or len(contacts)!=8:
        raise RuntimeError(json.dumps(audit,indent=2))
    folder = ROOT/'cad/packaging'
    fcstd = folder/'AQI_M03_Independent_Housing_STUDY.FCStd'
    step = folder/'AQI_M03_Independent_Housing_NOT_FOR_FABRICATION.step'
    doc.saveAs(str(fcstd)); Part.export(objects,str(step))
    reimport = Part.read(str(step))
    assert reimport.isValid() and len(reimport.Solids)==len(objects)
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(fcstd))
    assert all(o.Shape.isValid() for o in reopened.Objects if hasattr(o,'Shape'))
    App.closeDocument(reopened.Name)
    audit['native_reopen_and_STEP_reimport']='PASS'
    (folder/'M03_INDEPENDENT_HOUSING_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2))


if __name__=='__main__':
    build()
