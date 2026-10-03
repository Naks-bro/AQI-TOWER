"""Deployment sensitivities, not temperature certification or structural design."""
import json, math
from pathlib import Path
import d01_pressure as p
R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/component_validation'
p.C['guard_open_fraction']=.4*(300/320)**2
# Historical brochure curve retained for consistency; no assertion of lower bound.
def solve(extra):
    lo,hi=0.,4*95*p.CFM
    for _ in range(80):
        q=(lo+hi)/2
        loss=sum(p.budget(q,10).values())+extra*(q/300)**2
        if p.fan(q)>loss:lo=q
        else:hi=q
    return (lo+hi)/2
rows=[dict(assumed_extra_Pa_at300=x,calculated_flow_m3h=solve(x)) for x in (0,5,10,20)]
tip=[dict(assumed_mass_kg=m,assumed_CG_to_edge_m=.15,assumed_push_height_m=.631,
          incipient_static_tip_force_N=m*9.81*.15/.631) for m in (10,20,30)]
# A bounding rectangle including controls/studs is not the bearing footprint.
diameter=math.hypot(590,490)
data=dict(status='ASSUMPTIONS / REVIEW ONLY / NOT SAFETY OR PERFORMANCE VALIDATION',
    recorded_D01_envelope_mm=[590,490,631],
    rectangular_envelope_diagonal_mm=diameter,
    sleeve_ID_with_assumed_25mm_radial_clearance_mm=diameter+50,
    sleeve_note='Geometric packaging screen only; no wall, rain hood, airflow clearance or service space included.',
    temperature=dict(fan_OEM_max_C=40,IMD_Hyderabad_record_C=45.5,ambient_exceeds_fan_limit_C=5.5,
       proposed_indoor_test_inlet_ceiling_C=35,margin_to_fan_limit_C=5,
       caveat='35C is a proposed test-screening limit, not a validated thermal trip. All other component limits still apply.'),
    extra_weather_guard_loss_sensitivity=rows,
    tipping_illustrations=tip,
    tipping_caveat='Mass, centre of gravity, support polygon, friction, impact and anchor strength are unverified. No safety factor, wind or dynamic load included; not test loads or an anchor design.',
    tests=dict(baseline_R01_reproduced=abs(rows[0]['calculated_flow_m3h']-337.086432)<1e-5,
       extra_loss_reduces_flow=all(a['calculated_flow_m3h']>b['calculated_flow_m3h'] for a,b in zip(rows,rows[1:])),
       cylinder_contains_rectangle=diameter>590 and diameter>490,
       doubled_mass_doubles_static_moment=abs(tip[1]['incipient_static_tip_force_N']-2*tip[0]['incipient_static_tip_force_N'])<1e-10,
       OEM_limit_exceeded=45.5>40))
assert all(data['tests'].values())
(O/'deployment_screen.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2))
