"""Independent read-only audit of the generated fan case and extracted results."""
import hashlib
import json
import math
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
case = root/'cfd/V01_fan'
fan_path = root/'data/fans/systemair_KVO_250.json'
fan = json.loads(fan_path.read_text(encoding='utf-8'))
implementation = json.loads((case/'fan_implementation.json').read_text())
metrics = json.loads((root/'results/CFD_V01_FAN/metrics.json').read_text())
checks = {}
checks['source_curve_unchanged'] = hashlib.sha256(fan_path.read_bytes()).hexdigest() == implementation['source_json_sha256']
checks['source_points_unchanged'] = fan['fan_curve_points'] == implementation['source_points_unchanged']
checks['mesh_identical_to_V00'] = all(hashlib.sha256((case/'constant/polyMesh'/name).read_bytes()).hexdigest() == digest
    == hashlib.sha256((root/'cfd/V00/constant/polyMesh'/name).read_bytes()).hexdigest()
    for name,digest in implementation['mesh_file_sha256'].items())
audit = json.loads((case/'geometry_audit.json').read_text())
checks['CAD_unchanged'] = hashlib.sha256((root/'cad/parametric/AQI_Tower_ConceptA_V00.FCStd').read_bytes()).hexdigest() == audit['source_sha256']
checks['connected_valid_mesh'] = 'Mesh OK' in (case/'logs/checkMesh_kvo.log').read_text() and 'Number of regions: 1 (OK)' in (case/'logs/checkMesh_kvo.log').read_text()
checks['correct_volume_cell_count'] = metrics['cell_count'] == 57645 and math.isclose(metrics['fluid_volume_m3'],0.424,abs_tol=1e-7)
checks['ten_empty_zones'] = len(metrics['regions']) == 10 and sum(r['cells'] for r in metrics['regions'].values()) == 57645
u0=(case/'0/U').read_text()
checks['inlet_not_fixed_velocity'] = bool(re.search(r'AIR_INLET\s*\{\s*type pressureInletOutletVelocity;',u0))
checks['positive_flow_inside_curve'] = metrics['fan']['inside_source_curve'] and metrics['flow_m3_s']['inlet_outward_signed'] < 0
checks['mass_balance_within_0p1_percent'] = metrics['mass_imbalance_percent'] < 0.1
checks['fan_pressure_mapping_within_0p1_Pa'] = abs(metrics['fan']['curve_closure_error_Pa']) < 0.1
log = (case/'logs/foamRun_kvo.log').read_text() + '\n' + (case/'logs/foamRun_kvo_continue.log').read_text()
points = fan['fan_curve_points']
errors=[]
for q,p in re.findall(r'KVO250 Q=([\d.eE+-]+) Ps_Pa=([\d.eE+-]+)',log):
    q,p=float(q),float(p)
    if not 0 <= q <= points[-1]['Q_m3s']:
        continue
    segment=next((a,b) for a,b in zip(points,points[1:]) if a['Q_m3s'] <= q <= b['Q_m3s'])
    a,b=segment
    weight=(q-a['Q_m3s'])/(b['Q_m3s']-a['Q_m3s'])
    expected=(1-weight)*a['delta_P_static_Pa']+weight*b['delta_P_static_Pa']
    errors.append(abs(expected-p))
checks['logged_curve_matches_source'] = bool(errors) and max(errors)<1e-5
checks['final_log_clean_end'] = bool(re.search(r'\nEnd\s*$',(case/'logs/foamRun_kvo_continue.log').read_text()))
checks['residual_targets_met'] = metrics['criteria']['residuals']
report={'checks':checks,'max_logged_curve_error_Pa':max(errors),
        'numerical_convergence': 'CONVERGED' if checks['residual_targets_met'] else 'PARTIAL — NON-CONVERGED',
        'note':'Residual failure is reported, not concealed by mass conservation. Startup/exit errors retained.'}
(root/'results/CFD_V01_FAN/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert all(v for k,v in checks.items() if k!='residual_targets_met'), 'A setup/traceability check failed'
