"""Generate separate hollow transition/neck/outlet concept; no earlier CAD modified."""
import json
import math
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]


def square(side, z):
    h=side/2
    points=[App.Vector(-h,-h,z),App.Vector(h,-h,z),App.Vector(h,h,z),App.Vector(-h,h,z)]
    return Part.makePolygon(points+[points[0]])


def circle(diameter,z):
    return Part.Wire([Part.makeCircle(diameter/2,App.Vector(0,0,z))])


def build():
    c=json.loads((ROOT/'cad/parametric/airpath_m04_study.json').read_text(encoding='utf-8'))
    side=c['assumed_square_inlet_clear_side']; diameter=c['assumed_circular_clear_diameter']
    t=c['assumed_wall_thickness']; z=c['transition_base_z']; height=c['transition_height']
    if min(side,diameter,t,height,c['inlet_neck_length'],c['outlet_length']) <= 0:
        raise ValueError('Non-positive geometry input')
    doc=App.newDocument('AQI_M04_Airpath_STUDY')
    inside=Part.makeLoft([square(side,z),circle(diameter,z+height)],True,False)
    outside=Part.makeLoft([square(side+2*t,z),circle(diameter+2*t,z+height)],True,False)
    transition=outside.cut(inside)
    # Profile offset is not a uniform normal wall thickness; fabrication development required.
    def tube(start,length):
        return Part.makeCylinder(diameter/2+t,length,App.Vector(0,0,start)).cut(
            Part.makeCylinder(diameter/2,length,App.Vector(0,0,start)))
    shapes={'Transition':transition,'InletNeck':tube(z+height,c['inlet_neck_length']),
            'StraightOutlet':tube(c['outlet_base_z'],c['outlet_length'])}
    objects=[]
    for name,shape in shapes.items():
        if shape.isNull() or not shape.isValid() or len(shape.Solids)!=1:
            raise RuntimeError('Invalid hollow geometry: '+name)
        obj=doc.addObject('Part::Feature',name)
        obj.Label=name+' — ASSUMED GEOMETRY, no flanges/guard'
        obj.Shape=shape
        obj.addProperty('App::PropertyString','EvidenceStatus','Review')
        obj.EvidenceStatus=c['status']
        objects.append(obj)
    doc.recompute()
    out=ROOT/'cad/packaging'
    fcstd=out/'AQI_M04_Airpath_STUDY.FCStd'; step=out/'AQI_M04_Airpath_NOT_FOR_FABRICATION.step'
    doc.saveAs(str(fcstd)); Part.export(objects,str(step))
    imported=Part.read(str(step))
    assert imported.isValid() and len(imported.Solids)==3
    audit={'status':c['status'],'valid_solids':3,'STEP_reimport':'PASS',
           'side_wall_projection_angle_deg':round(math.degrees(math.atan((side-diameter)/2/height)),2),
           'inlet_neck_length_over_diameter':round(c['inlet_neck_length']/diameter,3),
           'outlet_length_over_diameter':round(c['outlet_length']/diameter,3),
           'wall_note':'Profiles offset by 2mm; normal wall thickness varies; not developed sheet metal',
           'assembly_note':'Coordinate study only; NOT integrated/fitted to OEM fan or mounting axes',
           'source_notes':c['notes']}
    (out/'M04_AIRPATH_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    App.closeDocument(doc.Name)
    reopened=App.openDocument(str(fcstd)); reopened.recompute()
    assert reopened.Transition.Shape.isValid()
    App.closeDocument(reopened.Name)
    print(json.dumps(audit,indent=2))


if __name__=='__main__':
    build()
