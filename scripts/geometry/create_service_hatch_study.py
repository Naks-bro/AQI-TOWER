"""New HEPA hatch/casing branch, preserving all prior CAD; envelopes not hardware."""
import hashlib
import json
from pathlib import Path
import FreeCAD as App
import Part

ROOT=Path(__file__).resolve().parents[2]


def build():
    c=json.loads((ROOT/'cad/parametric/hepa_service_hatch_m05.json').read_text(encoding='utf-8'))
    doc=App.newDocument('AQI_M05_HEPA_Service_Hatch_STUDY')
    objs=[]; hashes={}
    def add(name,shape,status='ASSUMED GEOMETRY'):
        if not shape.isValid() or len(shape.Solids)!=1:
            raise RuntimeError('Invalid hatch branch solid: '+name)
        o=doc.addObject('Part::Feature',name); o.Shape=shape
        o.addProperty('App::PropertyString','EvidenceStatus'); o.EvidenceStatus=status+' — NOT FOR FABRICATION'
        objs.append(o); return o
    def open_source(relative):
        path=ROOT/relative; hashes[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
        return App.openDocument(str(path))
    source=open_source('cad/packaging/AQI_M03_Independent_Housing_STUDY.FCStd')
    try:
        for o in source.Objects:
            if hasattr(o,'Shape') and o.Name not in {'Shell','HEPAServiceDoor','CleanHousing','CleanHousingServicePanel','PrefilterServiceDoor'}:
                add(o.Name,o.Shape.copy(),o.EvidenceStatus)
    finally:
        App.closeDocument(source.Name)
    source=open_source('cad/packaging/AQI_Cylindrical_Packaging_R02.FCStd')
    try:
        # In-memory parameter branch only. Do NOT save source or touch its on-disk CAD.
        source.Parameters.set('B1',str(c['casing_inner_diameter'])+' mm')
        source.recompute()
        window=Part.makeBox(c['outer_access_width'],1000,c['outer_access_height'],
                            App.Vector(-c['outer_access_width']/2,-1000,c['outer_access_z']))
        add('Shell',source.Shell.Shape.cut(window))
        add('HEPAServiceDoor',source.UnperforatedWall.Shape.common(window),'OUTER ACCESS PIECE; attachments UNKNOWN')
        add('PrefilterServiceDoor',source.PrefilterServiceDoor.Shape.copy())
    finally:
        App.closeDocument(source.Name)
    w,h,z=c['inner_opening_width'],c['inner_opening_height'],c['inner_opening_z']
    def panel(width,height,depth,front_y,bottom):
        return Part.makeBox(width,depth,height,App.Vector(-width/2,front_y,bottom))
    clean=Part.makeBox(653,653,318,App.Vector(-326.5,-326.5,645)).cut(
        Part.makeBox(649,649,318,App.Vector(-324.5,-324.5,645)))
    opening=panel(w,h,12,-332.5,z)
    add('CleanHousing',clean.cut(opening))
    land=c['flange_land']; ft=c['flange_thickness']; gt=c['gasket_installed_envelope']; ct=c['cover_thickness']
    flange_y=-326.5-ft; gasket_y=flange_y-gt; cover_y=gasket_y-ct
    flange=panel(w+2*land,h+2*land,ft,flange_y,z-land).cut(panel(w,h,ft,flange_y,z))
    gasket_land=c['gasket_land']
    gasket=panel(w+2*gasket_land,h+2*gasket_land,gt,gasket_y,z-gasket_land).cut(panel(w,h,gt,gasket_y,z))
    add('HatchFlange',flange,'ILLUSTRATIVE MOUNTING FRAME; joins UNKNOWN')
    add('HatchGasketEnvelope',gasket,'INSTALLED SPACE ONLY; compression and material UNKNOWN')
    cover=add('HatchCover',panel(w+2*land,h+2*land,ct,cover_y,z-land))
    moving=['HatchCover']
    for j,cz in enumerate((z-land/2,z+h+land/2)):
        for i,x in enumerate(c['latch_locations_x']):
            name=f'LatchLocation{j+1}_{i+1}'
            shape=Part.makeBox(c['latch_envelope_width'],c['latch_forward_projection'],c['latch_envelope_height'],
                               App.Vector(x-c['latch_envelope_width']/2,cover_y-c['latch_forward_projection'],cz-c['latch_envelope_height']/2))
            add(name,shape,'GENERIC LATCH LOCATION BLOCK; not a mechanism'); moving.append(name)
    for i,x in enumerate((-100,100)):
        name=f'HandleLocation{i+1}'
        add(name,Part.makeBox(20,c['handle_forward_projection'],30,
                              App.Vector(x-10,cover_y-c['handle_forward_projection'],790)),
            'GENERIC HANDLE LOCATION; grip/hand clearance UNKNOWN'); moving.append(name)
    doc.recompute()
    conflicts=[]
    for i,a in enumerate(objs):
        for b in objs[i+1:]:
            overlap=a.Shape.common(b.Shape).Volume
            if overlap>1e-4:
                conflicts.append({'first':a.Name,'second':b.Name,'overlap_mm3':round(overlap,4)})
    sweep_clashes={}
    service_ignore=set(moving)|{'HEPAServiceDoor','HEPAEnvelope','HEPARetainerEnvelope'}
    for name,sweep in {
        'HEPA_lifted':Part.makeBox(593,1100,292,App.Vector(-296.5,-803.5,653)),
        'retainer_clamps_already_removed':Part.makeBox(633,1100,5,App.Vector(-316.5,-783.5,940))}.items():
        sweep_clashes[name]=[o.Name for o in objs if o.Name not in service_ignore and o.Shape.common(sweep).Volume>1e-4]
    # Straight forward translation with decorative outer access piece already removed.
    extraction=[]
    for name in moving:
        o=doc.getObject(name); box=o.Shape.BoundBox
        swept=Part.makeBox(box.XLength,box.YLength+400,box.ZLength,
                           App.Vector(box.XMin,box.YMin-400,box.ZMin))
        for fixed in objs:
            if fixed.Name in set(moving)|{'HEPAServiceDoor'}:
                continue
            if fixed.Shape.common(swept).Volume>1e-4:
                extraction.append({'moving':name,'fixed':fixed.Name})
    for relative,digest in hashes.items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest
    audit={'status':c['status'],'valid_solids':len(objs),'positive_volume_clashes':conflicts,
           'assumed_filter_service_sweep_clashes':sweep_clashes,'assumed_cover_forward_removal_clashes':extraction,
           'casing_inner_diameter_mm_ASSUMED':c['casing_inner_diameter'],'outer_access_width_mm_ASSUMED':c['outer_access_width'],
           'inner_opening_mm_ASSUMED':[w,h],'retainer_nominal_side_margin_mm':(w-633)/2,
           'gasket_installed_envelope_mm_NOT_COMPRESSION':gt,
           'latch_location_count_NOT_SELECTED_HARDWARE':8,
           'cover_steel_mass_kg_ASSUMED':cover.Shape.Volume*1e-9*7850,
           'door_pressure_force_N_at_ASSUMED_500Pa':500*(w/1000)*(h/1000),
           'pressure_note':'Assumed LOCAL door differential, not known HEPA pressure or latch preload',
           'source_sha256_unchanged':hashes,'notes':c['notes']}
    if conflicts or any(sweep_clashes.values()) or extraction:
        raise RuntimeError(json.dumps(audit,indent=2))
    folder=ROOT/'cad/packaging'; fcstd=folder/'AQI_M05_HEPA_Service_Hatch_STUDY.FCStd'
    step=folder/'AQI_M05_HEPA_Service_Hatch_NOT_FOR_FABRICATION.step'
    doc.saveAs(str(fcstd)); Part.export(objs,str(step))
    check=Part.read(str(step)); assert check.isValid() and len(check.Solids)==len(objs)
    App.closeDocument(doc.Name)
    reopened=App.openDocument(str(fcstd)); assert all(o.Shape.isValid() for o in reopened.Objects if hasattr(o,'Shape'))
    App.closeDocument(reopened.Name)
    audit['native_reopen_and_STEP_reimport']='PASS'
    (folder/'M05_HEPA_HATCH_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2))


if __name__=='__main__':
    build()
