"""OEM relay screening and idealized architecture counterexamples, not wiring design."""
from itertools import permutations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/prototype_d01/electrical_package'
def screen():
    candidates=[
      dict(part='Pilz 774326 / PNOZ X5',voltage=12,watts=2.5,dimensions_mm=[87,22.5,121],
           source='https://www.pilz.com/en-INT/eshop/product/774326',
           limitation='Manual start listed; monitored held-button rejection not established. Not selected.'),
      dict(part='Pilz 777607 / PNOZ X9P',voltage=12,watts=7,dimensions_mm=[94,90,121],
           source='https://www.pilz.com/en-INT/eshop/product/777607',
           limitation='Monitored start listed, but nearly consumes nominal supply margin; no suitable enclosure fit. Not selected.'),
      dict(part='Pilz 750104 / PNOZ s4',voltage=24,watts=2.5,dimensions_mm=[98,22.5,120],
           source='https://www.pilz.com/en-US/eshop/product/750104',
           manual='https://www.pilz.com/download/open/PNOZ_s4_Operat_Man_21396-EN-17.pdf',
           limitation='Monitored edge start documented; wrong supply voltage for existing12V rail. Additional supply, sequence and fault monitoring needed. Not selected.')]
    reservation=(140,100,40)
    for p in candidates:
        p['fits_in_normal_DIN_orientation_before_clearance']=p['dimensions_mm'][2]<=40
        p['axis_aligned_body_only_fits']=[dict(orientation_mm=d,remaining_mm=[r-x for r,x in zip(reservation,d)])
            for d in permutations(p['dimensions_mm']) if all(x<=r for x,r in zip(d,reservation))]
        p['fit_warning']='Reservation is not internal usable enclosure size. Body fit excludes rail, wiring, bend radius, terminals, ventilation, controller and hub.'
        if p['voltage']==12:
            p['fan_plus_relay_nominal_W']=16.8+p['watts']
            p['remaining_supply_W_before_auxiliaries']=24-p['fan_plus_relay_nominal_W']
            p['fan_plus_relay_at_assumed_1_25_fan_multiplier_W']=16.8*1.25+p['watts']
        else:
            p['direct_12V_supply_compatible']=False
    # Idealized latched upstream run contact. No timing or OEM behavior is asserted.
    events=[('Running',True,True,True),('Fan supply absent',True,False,True),
            ('Fan supply returns',True,True,True)]
    supply_trace=[dict(event=e,run_contact_closed=k,fan_supply_good=p,hub_path_good=h,
                       fan_power_available=k and p and h) for e,k,p,h in events]
    hub_events=[('Running',True,True,True),('Hub output absent',True,True,False),
                ('Hub output recovers',True,True,True)]
    hub_trace=[dict(event=e,run_contact_closed=k,fan_supply_good=p,hub_path_good=h,
                   fan_power_available=k and p and h) for e,k,p,h in hub_events]
    checks={
      'X9P_remaining_only_0_2W':abs(candidates[1]['remaining_supply_W_before_auxiliaries']-.2)<1e-9,
      'X5_remaining_4_7W':abs(candidates[0]['remaining_supply_W_before_auxiliaries']-4.7)<1e-9,
      'X9P_over_24W_at_assumed_1_25':candidates[1]['fan_plus_relay_at_assumed_1_25_fan_multiplier_W']>24,
      'no_normal_DIN_depth_fit':not any(p['fits_in_normal_DIN_orientation_before_clearance'] for p in candidates),
      'rotated_s4_body_fit_not_denied':bool(candidates[2]['axis_aligned_body_only_fits']),
      'X9P_no_axis_aligned_fit':not candidates[1]['axis_aligned_body_only_fits'],
      'upstream_contact_does_not_prevent_recovery_restart':not supply_trace[1]['fan_power_available'] and supply_trace[2]['fan_power_available'],
      'upstream_voltage_cannot_see_hub_output_loss':all(t['fan_supply_good'] for t in hub_trace) and not hub_trace[1]['fan_power_available'] and hub_trace[2]['fan_power_available']}
    assert all(checks.values())
    return dict(accessed='2026-10-04',status='NO COMPLETE PROTECTIVE ASSEMBLY SELECTED',
      candidates=candidates,checks=checks,
      counterexamples={'separate_control_supply':supply_trace,'downstream_recovery':hub_trace},
      limitations='Idealized possible failure paths, not measured OEM reset behavior. Relay contact load suitability, input monitoring, power-converter requirements, protective reliability and wiring not verified.')

if __name__=='__main__':
    data=screen();(OUT/'PROTECTIVE_CANDIDATE_SCREEN.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps(data,indent=2))
