"""Transparent partial mass and stability/tolerance sensitivities, NOT release tests."""
import json,math,csv
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/mechanical_package'
items=json.loads((O/'part_inventory.json').read_text());mass=[];omitted=[]
for p in items:
    n=p['id'];rho=None
    if p['kind']=='panel':rho=650
    elif n.startswith('M07_'):rho=600
    elif p['kind'] in ('hardware','guard') or n.startswith('A07_'):rho=7850
    if rho is None:omitted.append(n);continue
    mass.append(dict(id=n,density_assumed_kg_m3=rho,mass_kg=p['volume_mm3']*1e-9*rho,centre_mm=p['centre_mm']))
subtotal=sum(p['mass_kg'] for p in mass)
centre=[sum(p['mass_kg']*p['centre_mm'][k] for p in mass)/subtotal for k in range(3)]
# Hypothetical WHOLE mass, centred at x275/y180. Not the partial CAD centroid.
cases=[dict(assumed_whole_mass_kg=m,front_back_tip_force_N=m*9.81*.165/.631,side_tip_force_N=m*9.81*.25/.631) for m in (10,15,20,25)]
seal=[dict(assumed_filter_thickness_mm=t,installed_gasket_gap_mm=43-t,compression_if_free4mm_percent=100*(4-(43-t))/4) for t in (39,40,41)]
tests=dict(mass_positive=subtotal>0,all_omitted_present=bool(omitted),support_depth_smaller_than_width=.165<.25,
    tipping_scales_with_mass=abs(cases[2]['front_back_tip_force_N']-2*cases[0]['front_back_tip_force_N'])<1e-9,
    tolerance_changes_compression=seal[0]['compression_if_free4mm_percent']==0 and seal[2]['compression_if_free4mm_percent']==50,
    fan_nominal_stack=50-(1+27+1+9+1+5)==6,
    M5_side_projection=39-(29+1.2+5)>1.6,
    M5_centre_projection=19-(9+1.2+5)>1.6)
assert all(tests.values())
out=dict(status='ASSUMED MATERIALS / PARTIAL MASS / NO STRUCTURAL PASS',
    densities_assumed_kg_m3=dict(panels=650,cleats=600,metal=7850),
    partial_subtotal_kg=subtotal,partial_centroid_mm=centre,omitted_objects=omitted,
    caveats='No actual whole-device mass/CG. Guard perforations omitted in CAD, so full-sheet proxy overstates that part of assumed mass; threads/welds/coatings omitted. Foot, fan, filter, seals and control masses excluded. No strength allowables supplied.',
    hypothetical_stability=dict(support_polygon_mm=[25,525,15,345],force_height_mm=631,assumed_CG_xy_mm=[275,180],cases=cases,
        caveat='Static tipping balance only; no safety factor, impact, sliding, floor unevenness or cable pull. Not public-use qualification.'),
    seal_tolerance_sensitivity=seal,seal_note='Filter39/40/41 and gasket4mm free are assumptions. Fixed43mm nominal gap does NOT guarantee safe compression. Verify actual material/force and thickness before cutting sleeves.',
    tests=tests)
(O/'mechanical_screen.json').write_text(json.dumps(out,indent=2))
with (O/'ASSUMED_PARTIAL_MASS.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(mass[0]));w.writeheader();w.writerows(mass)
print(json.dumps(out,indent=2))
