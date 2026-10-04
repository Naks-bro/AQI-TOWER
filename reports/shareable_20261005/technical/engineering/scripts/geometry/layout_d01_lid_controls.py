"""E04 derivative of E03: original button proxies, never OEM manufacturing CAD.

Requires locally downloaded OEM box STEP and existing E03 evidence/CAD.
All rear envelopes and wire tails are assumptions, NOT assembled OEM dimensions.
"""
from pathlib import Path
import hashlib, json
import FreeCAD as A
import Part

R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
oem_path=R/'tmp/control_oem/step/1554XA2GY.stp'
oem=Part.read(str(oem_path))
assert len(oem.Solids)==24
e03=json.loads((O/'FIT_CHECKS.json').read_text())
tower=R/'reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd'
tower_hash=hashlib.sha256(tower.read_bytes()).hexdigest()
assert tower_hash==e03['native_tower_sha256']
doc=A.openDocument(str(O/'D01_E03_CONTROL_ENVELOPES.FCStd'))
assert len(doc.Objects)==9
V=A.Vector
buttons=[('START',-15,'ZB5AA3','ZBE1016','NO','#148b69','I1','A0'),
         ('STOP',45,'ZB5AA4','ZBE1026','NC','#d54451','I2','A1'),
         ('RESET',105,'ZB5AA6','ZBE1016','NO','#4276c1','I3','A2')]
records=[]
def add(name,shape,note):
    obj=doc.addObject('PartDesign::Feature',name); obj.Shape=shape
    obj.addProperty('App::PropertyString','EvidenceStatus'); obj.EvidenceStatus=note
    return obj
for name,x,head,contact,kind,color,terminal,pin in buttons:
    line=Part.makeLine(V(x,0,-20),V(x,0,60))
    levels=sorted(v.Point.z for edge in oem.Solids[1].common(line).Edges for v in edge.Vertexes)
    assert len(levels)==2 and abs(levels[0]-46)<.01 and abs(levels[1]-50)<.01
    rear=Part.makeBox(40,40,55,V(x-20,-20,-9))
    tail=Part.makeBox(40,40,20,V(x-20,-20,-29))
    add(name+'_FACE_PROXY',Part.makeCylinder(14.5,8,V(x,0,50)),
        '29mm head width from OEM; round face and 8mm projection ASSUMED')
    add(name+'_REAR_ASSUMED',rear,'ASSUMED40x40x55 below inner lid; not assembled OEM dimensions')
    add(name+'_WIRE_TAIL_ASSUMED',tail,'ASSUMED20mm additional depth; not verified bend radius')
    actual_hits=[]
    for idx,solid in enumerate(oem.Solids):
        for category,shape in [('rear',rear),('wire_tail',tail)]:
            volume=shape.common(solid).Volume
            if volume>.01:actual_hits.append({'category':category,'OEM_solid':idx,'volume_mm3':volume})
    body_gaps={n:rear.fuse(tail).distToShape(doc.getObject(n).Shape)[0]
               for n in ('CTRL1_OPTA_LITE','H1_NA_FH1','SC1_NA_FC1')}
    service_overlaps={n:rear.fuse(tail).common(doc.getObject(n).Shape).Volume
                     for n in ('CTRL1_WIRE_SPACE_ASSUMED','H1_CONNECTOR_SPACE_ASSUMED','SC1_CONNECTOR_SPACE_ASSUMED')}
    assert not actual_hits, actual_hits
    assert all(g>.01 for g in body_gaps.values()),body_gaps
    # Proposed cut in original proxy only, not the private OEM file.
    shell=doc.getObject('CB1_SIMPLIFIED_ENVELOPE')
    shell.Shape=shell.Shape.cut(Part.makeCylinder(11.15,10,V(x,0,45)))
    records.append(dict(name=name,centre_mm=[x,0],head=head,collar='ZB5AZ009',contact=contact,
        contact_type=kind,terminal=terminal,firmware_pin=pin,color=color,
        lid_surface_levels_mm=levels,lid_local_thickness_mm=levels[1]-levels[0],
        rear_assumed_bounds_mm=[x-20,-20,-9,x+20,20,46],
        wire_tail_assumed_bounds_mm=[x-20,-20,-29,x+20,20,-9],
        OEM_collision_hits=actual_hits,minimum_body_gaps_mm=body_gaps,
        assumed_service_overlap_mm3=service_overlaps))
assert all(doc.Objects[i].Shape.isValid() for i in range(len(doc.Objects)))
doc.recompute(); doc.saveAs(str(O/'D01_E04_LID_CONTROL_ENVELOPES.FCStd'))
Part.export(list(doc.Objects),str(O/'D01_E04_LID_CONTROL_ENVELOPES.step'))
step=O/'D01_E04_LID_CONTROL_ENVELOPES.step'
step.write_text('\n'.join(line.rstrip() for line in step.read_text().splitlines())+'\n')
A.closeDocument(doc.Name)
check=A.openDocument(str(O/'D01_E04_LID_CONTROL_ENVELOPES.FCStd'))
assert len(check.Objects)==18 and all(o.Shape.isValid() for o in check.Objects)
A.closeDocument(check.Name)
assert len(Part.read(str(step)).Solids)==18
data=dict(release=False,physical_tests=0,access_date='2026-10-05',
    status='PROPOSED CLOSED-LID ORDINARY CONTROLS / NOT DRILLING OR WIRING RELEASE',
    native_tower_sha256=tower_hash,native_tower_unchanged=tower_hash==hashlib.sha256(tower.read_bytes()).hexdigest(),
    OEM_box_sha256=hashlib.sha256(oem_path.read_bytes()).hexdigest(),objects=18,buttons=records,
    pitch_mm=60,proposed_hole_diameter_mm=22.3,hole_upper_tolerance_mm=.4,
    OEM_mount_panel_range_mm=[1,6],
    input_screen={'nominal_voltage_V':12,'OEM_impedance_ohm':8900,
       'nominal_resistance_screen_mA':12/8900*1000,'guaranteed_current_mA':None,
       'OEM_current_at_10V_mA':1.12,'OEM_HIGH_min_V':6.6,'OEM_LOW_max_V':4.46},
    contact_minimum_switching_voltage_current='UNKNOWN; gold-flashed low-power designation verified only',
    sources={'mounting':'https://download.se.com/files?p_Doc_Ref=BRU46063',
      'low_power_catalogue':'https://iportal.se.com/Contents/docs/DIA5ED2121213EN.PDF',
      'green_head':'https://www.clipsal.com/products/industrial/harmony/push-button-head-plastic-flush-green-22mm-spring-return-unmarked-zb5aa3?itemno=ZB5AA3',
      'collar_CAD':'https://download.se.com/files?p_Doc_Ref=MCADID0005208_3D-CAD',
      'opta':e03['sources']['opta'],'box':e03['sources']['box']},
    limitations=['Rear stack55mm and wire tail20mm are deliberately ASSUMED reservations, not OEM assembly fit proof',
      'Wire-tail reservations overlap existing assumed speed-controller service space; actual routing must resolve this',
      'Local OEM lid thickness4mm at centres only; gasket, mounting torque, labels and sealing must be reviewed before drilling',
      'Low-current numeric contact rating, terminal identifiers, leads, source protection and terminals not released',
      'STOP is ordinary software input, not emergency stop or isolation; RESET never substitutes for protective restart',
      'NA-FC1 remains internal: set only while source disconnected and lid closed before operation; no powered open-box adjustment',
      'Protection, guards, mounts, source/harness and heat remain open; default firmware relay outputs remain disabled'])
(O/'LID_CONTROL_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,indent=2))
