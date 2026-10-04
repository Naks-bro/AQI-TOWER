"""Screening only: four parallel fans / two parallel filters. No measured CADR."""
import json, math, csv
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01'
C=json.loads((R/'cad/parametric/d01_r00.json').read_text())
CFM=1.69901079552; MMH2O=9.80665
def interp(x,xs,ys):
    if x<=xs[0]:return ys[0]
    if x>=xs[-1]:return ys[-1]
    for i in range(1,len(xs)):
        if x<=xs[i]:return ys[i-1]+(ys[i]-ys[i-1])*(x-xs[i-1])/(xs[i]-xs[i-1])
def fan(q,offset=0):
    return max(0,interp(q/4/CFM,C['fan_curve_cfm'],C['fan_curve_mmH2O'])*MMH2O+offset)
def budget(q,filter_ref):
    vfan=(q/3600)/(4*math.pi*(C['fan_aperture']/2000)**2)
    vg=(q/3600)/(.320*.320*C['guard_open_fraction'])
    return {'filter_path':filter_ref*q/400,
            'intake_and_plenum':C['plenum_K_on_total_fan_aperture']*C['rho_kg_m3']/2*vfan*vfan,
            'inner_guard':C['guard_K_on_free_area_each']*C['rho_kg_m3']/2*vg*vg,
            'outer_guard':C['guard_K_on_free_area_each']*C['rho_kg_m3']/2*vg*vg,
            'installation_reserve':C['rho_kg_m3']/2*vfan*vfan}
def solve(ref,offset=0):
    a,b=0,4*95*CFM
    for _ in range(70):
        m=(a+b)/2
        if fan(m,offset)>sum(budget(m,ref).values()):a=m
        else:b=m
    return (a+b)/2
def main():
    O.mkdir(parents=True,exist_ok=True)
    scenarios=[]
    for name,p in C['filter_scenarios_Pa_at_400_m3h_total'].items():
        q=solve(p);loss=budget(q,p)
        scenarios.append(dict(name=name,assumed_filter_Pa_at400=p,flow_m3h=q,fan_Pa=fan(q),budget_Pa=loss,curve_minus2Pa_flow=solve(p,-2),curve_plus2Pa_flow=solve(p,2),closure_error_Pa=fan(q)-sum(loss.values())))
    tests={
      'conversion_mmH2O':abs(MMH2O-9.80665)<1e-8,
      'zero_flow_all_losses_zero':sum(budget(0,10).values())==0,
      'parallel_fans_same_pressure':abs(fan(4*50*CFM)-2.5*MMH2O)<1e-8,
      'two_filters_NOT_added':budget(400,10)['filter_path']==10,
      'filter_linear':budget(200,10)['filter_path']==5,
      'guard_quadratic':abs(budget(400,10)['inner_guard']/budget(200,10)['inner_guard']-4)<1e-8,
      'loaded_flow_lower':scenarios[2]['flow_m3h']<scenarios[1]['flow_m3h']<scenarios[0]['flow_m3h'],
      'all_intersections_close':all(abs(s['closure_error_Pa'])<1e-7 for s in scenarios),
      'nominal_electrical_budget':4*C['fan_nominal_current_A']<C['supply_current_A']
    }
    assert all(tests.values()),tests
    result=dict(status='ASSUMED SCENARIOS, NOT PERFORMANCE CLAIMS',scenarios=scenarios,tests=tests,nominal_fan_current_A=1.4,nominal_fan_power_W=16.8,supply_max_W=24,nominal_headroom_W=7.2,notes=['Controller overhead and startup transient not measured.','Guard geometry and K values assumed. Installation reserve is a conservative allowance, not a verified static/total pressure conversion.','No prefilter, HEPA, carbon, water, duct or cosmetic cylinder installed. Adding them invalidates this model.','Equal parallel flow and no bypass assumed; fan-curve digitization +/-2Pa is not total uncertainty.','Filter reference dimensions are OEM; resistance scenarios are not OEM data.','No CADR, efficiency, outdoor radius or noise prediction.'])
    (O/'pressure_results.json').write_text(json.dumps(result,indent=2))
    with (O/'pressure_curves.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['total_flow_m3h','fan_available_Pa','low_clean_Pa','middle_clean_Pa','loaded_sensitivity_Pa'])
        for q in range(0,647,5):w.writerow([q,fan(q),*[sum(budget(q,p).values()) for p in (5,10,20)]])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
