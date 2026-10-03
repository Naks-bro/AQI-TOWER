"""R01 loss update and conditional bracket load arithmetic; no physical release."""
import json,sys,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/r01'
import d01_pressure as p
p.O=O;p.C=dict(p.C);p.C['guard_open_fraction']=.40*(300/320)**2
p.main()
data=json.loads((O/'pressure_results.json').read_text())
data['revision']='D01-R01';data['guard_open_area_m2_each']=.3*.3*.4
data['notes']+=['R01:10mm solid border on320mm guard face leaves300x300 perforated field,40% porosity assumed. Guard K remains unmeasured.','Do not use R00 airflow numbers for this revised guard.']
(O/'pressure_results.json').write_text(json.dumps(data,indent=2))
def strip_stress(force,arm,width,thickness):return force*arm/(width*thickness**2/6)
loads={
 'guard':{'assumed_force_N':50,'assumed_arm_mm':10,'width_mm':40,'thickness_mm':2,'nominal_bending_MPa':strip_stress(50,10,40,2)},
 'shelf':{'assumed_filter_mass_kg':2,'assumed_handling_factor':2,'single_bracket_force_N':2*9.81*2,'assumed_arm_mm':25,'width_mm':30,'thickness_mm':2,'nominal_bending_MPa':strip_stress(2*9.81*2,25,30,2)},
 'limitations':'Illustrative load cases, NOT prescribed safety tests. Conservative single-bracket shelf share. Simple straight-strip bending ignores bend radius, holes, torsion, connections and guard-panel flexure. Material strength, fastener capacities and allowable stresses not established. No PASS.'}
tests={'porosity_reduced':math.isclose(p.C['guard_open_fraction'],.3515625),'open_area':math.isclose(.32*.32*p.C['guard_open_fraction'],.036),'flow_order':data['scenarios'][2]['flow_m3h']<data['scenarios'][1]['flow_m3h']<data['scenarios'][0]['flow_m3h'],'guard_bending_arithmetic':math.isclose(loads['guard']['nominal_bending_MPa'],18.75),'shelf_bending_arithmetic':math.isclose(loads['shelf']['nominal_bending_MPa'],49.05)}
assert all(tests.values());(O/'load_screening.json').write_text(json.dumps({'loads':loads,'tests':tests},indent=2))
print(json.dumps({'R01_guard_free_area_m2':.036,'R01_flows_m3h':[s['flow_m3h'] for s in data['scenarios']],'tests':tests},indent=2))
