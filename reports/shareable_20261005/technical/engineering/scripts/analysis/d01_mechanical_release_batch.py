"""CAD-derived fit requirements and statically balanced joint-demand screens.

Standard library only. No material allowable, test force or release is invented.
All illustrated tolerance/load cases are ASSUMPTIONS, not fabrication settings.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'reports/prototype_d01/mechanical_package'
OUT = BASE / 'batch_closure'


def interval(lo, hi, positive=False):
    if not all(math.isfinite(x) for x in (lo, hi)) or lo > hi or (positive and lo <= 0):
        raise ValueError('Finite ordered intervals required; thickness must be positive')
    return lo, hi


def seal_window(filter_mm, free_gasket_mm, compression_fraction, gap_error_mm):
    """G=t+f(1-c). Include signed gap/flatness error bounded by +/- error.

    Returns nominal stop-gap interval satisfying EVERY independent tolerance
    corner. No gasket stress law is inferred from compression percentage.
    """
    t0, t1 = interval(*filter_mm, positive=True)
    f0, f1 = interval(*free_gasket_mm, positive=True)
    c0, c1 = interval(*compression_fraction)
    if c0 < 0 or c1 >= 1 or not math.isfinite(gap_error_mm) or gap_error_mm < 0:
        raise ValueError('Compression 0 <= min <= max < 1; error finite and nonnegative')
    lower = t1 + f1 * (1-c1) + gap_error_mm
    upper = t0 + f0 * (1-c0) - gap_error_mm
    return dict(nominal_gap_lower_mm=lower, nominal_gap_upper_mm=upper,
                robust_fixed_stop_possible=lower <= upper,
                window_width_mm=upper-lower,
                nominal_gap_midpoint_mm=(lower+upper)/2 if lower <= upper else None)


def compression_bounds(gap_mm, filter_mm, free_gasket_mm, error_mm=0):
    t0, t1 = interval(*filter_mm, positive=True)
    f0, f1 = interval(*free_gasket_mm, positive=True)
    if not math.isfinite(gap_mm) or not math.isfinite(error_mm) or error_mm < 0:
        raise ValueError('Finite gap and nonnegative error required')
    # Exhaust all corners: valid even when filter exceeds stop gap.
    vals = [1-(g-t)/f for g in (gap_mm-error_mm, gap_mm+error_mm)
            for t in (t0,t1) for f in (f0,f1)]
    return dict(min_fraction=min(vals), max_fraction=max(vals),
                interpretation='Negative = uncompressed gap; >1 = impossible geometric overclosure')


def joint_demands(points_mm, force_N, moment_Nmm):
    """In-plane linear equal-stiffness bolt group; no friction/preload credit.

    Force components and moment about group centroid. Only a DEMAND calculation:
    no pull-through, withdrawal, out-of-plane prying or panel stress solution.
    """
    if len(points_mm) < 2 or not all(math.isfinite(x) for p in points_mm for x in p):
        raise ValueError('At least two finite points required')
    if not all(math.isfinite(x) for x in (*force_N, moment_Nmm)):
        raise ValueError('Finite loads required')
    n = len(points_mm)
    centre = [sum(p[k] for p in points_mm)/n for k in (0,1)]
    relative = [(p[0]-centre[0], p[1]-centre[1]) for p in points_mm]
    polar = sum(x*x+y*y for x,y in relative)
    if polar <= 0:
        raise ValueError('Distinct group positions required')
    forces = [(force_N[0]/n-moment_Nmm*y/polar,
               force_N[1]/n+moment_Nmm*x/polar) for x,y in relative]
    return dict(centroid_mm=centre, sum_r_squared_mm2=polar,
                force_vectors_N=forces, peak_resultant_N=max(math.hypot(*f) for f in forces),
                recovered_force_N=[sum(f[k] for f in forces) for k in (0,1)],
                recovered_moment_Nmm=sum(x*f[1]-y*f[0] for (x,y),f in zip(relative,forces)))


def bounds(part):
    return [[min(v[k] for v in part['vertices']), max(v[k] for v in part['vertices'])] for k in range(3)]


def calculate():
    mesh_path = BASE/'cad_mesh.json'
    mesh = {p['name']: p for p in json.loads(mesh_path.read_text())}
    sides = {}
    for side, rear in [('Front',False), ('Rear',True)]:
        reducer = bounds(mesh['A01_Reducer_'+side])
        retainer = bounds(mesh['A04_Retainer_'+side])
        gasket = bounds(mesh['A02_Filter_gasket_'+side])
        filt = bounds(mesh['A03_STARKVIND_envelope_'+side])
        gap = retainer[1][0]-reducer[1][1] if rear else reducer[1][0]-retainer[1][1]
        sleeve = bounds(mesh[f'K04_Inner_stop_{rear}_0'])
        length = sleeve[1][1]-sleeve[1][0]
        sides[side] = dict(nominal_stop_gap_mm=gap, modeled_filter_thickness_mm=filt[1][1]-filt[1][0],
                           modeled_installed_gasket_mm=gasket[1][1]-gasket[1][0],
                           modeled_inner_sleeve_mm=length, gap_minus_sleeve_mm=gap-length,
                           reducer_y_faces_mm=reducer[1], retainer_y_faces_mm=retainer[1])
    scenarios = []
    for name,t,f,c,e in [
        ('historical_thickness_sensitivity',[39,41],[4,4],[.20,.40],.25),
        ('illustrative_matched_parts',[39.9,40.1],[3.9,4.1],[.20,.40],.10),
        ('illustrative_wider_gasket_tolerance',[39.9,40.1],[3.5,4.5],[.20,.40],.10)]:
        result=seal_window(t,f,c,e)
        midpoint=result['nominal_gap_midpoint_mm']
        scenarios.append(dict(id=name,basis='ASSUMED independent bounds; not OEM limits or selected material',
                              filter_mm=t,free_gasket_mm=f,compression_fraction=c,gap_error_mm=e,
                              result=result,current_43mm_compression=compression_bounds(43,t,f,e),
                              candidate_sleeve_mm=midpoint-sides['Front']['gap_minus_sleeve_mm'] if midpoint is not None else None))
    groups={}
    for prefix,plane in [('K06_End_False_', (1,2)),('K06_End_True_', (1,2)),
                         ('K07_Seat_False_', (0,2)),('K07_Seat_True_', (0,2))]:
        members=[p for name,p in mesh.items() if name.startswith(prefix) and name.endswith('_screw')]
        pts=[]
        for p in members:
            b=bounds(p);pts.append([(b[k][0]+b[k][1])/2 for k in plane])
        cases=[]
        for force,eccentricity in [(10,0),(30,0),(60,0),(30,100)]:
            cases.append(dict(assumed_vertical_force_N=force,assumed_horizontal_eccentricity_mm=eccentricity,
                              result=joint_demands(pts,[0,-force],-force*eccentricity)))
        groups[prefix]=dict(plane_axes=['xyz'[k] for k in plane], bolt_count=len(pts), centres_mm=pts,
                            assumed_group_load_cases=cases)
    inventory=json.loads((BASE/'part_inventory.json').read_text())
    byname={p['id']:p for p in inventory}
    gasket=byname['A02_Filter_gasket_Front']
    # Exact modeled ring volume / its modeled installed thickness, not gross filter rectangle.
    ring_area=gasket['volume_mm3']/sides['Front']['modeled_installed_gasket_mm']
    fan_pairs=[p for n,p in mesh.items() if n.startswith('K02_') and n.endswith('_screw')]
    native=BASE/'D01_R03M_ASSEMBLY.FCStd'
    return dict(status='DIGITAL REQUIREMENTS SCREEN / NOT FABRICATION OR SAFETY APPROVAL',
                input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                               (mesh_path,BASE/'part_inventory.json',BASE/'fasteners.json',native)},
                cad_filter_stacks=sides, seal_scenarios=scenarios, cad_gasket_contact_area_mm2=ring_area,
                clamp_force_relationship=dict(total_N='selected gasket compression stress MPa * modeled ring area mm2',
                    modeled_ring_area_mm2=ring_area, stress_MPa=None, installed_total_force_N=None,
                    note='Uniform contact assumption; adhesive, corners, seams and actual compression law unknown'),
                cabinet_groups=groups, cad_fan_screw_count=len(fan_pairs),
                actual_service_loads_N=None, actual_material_allowables_MPa=None,
                guard_strength_status='OPEN: actual perforated plate, welded skirt/brackets, attachment and probe criteria not evaluated',
                digital_gaps_closed=['Actual front/rear stop stack independently extracted from saved mesh',
                    'Robust fixed-stop feasibility and measurable sleeve adjustment solved for supplied tolerance bounds',
                    'Actual cabinet bolt groups extracted with force/moment equilibrium checks',
                    'Selected seal force retained as unknown rather than pressure-derived clamp force'],
                physical_release_open=['Exact filter delivered thickness/frame tolerance and compression strength',
                    'Selected gasket free thickness tolerance, compression window, force/relaxation/adhesive data',
                    'Measured reducer/retainer flatness and assembled stop gap; seam/feedthrough leak integrity',
                    'Selected plywood/cleat grades, fastener threads/grades/torque and withdrawal/bearing design',
                    'Cabinet racking, guard perforated plate/weld/attachment/probe and stability review',
                    'Full installed mass/CG, foot contact/friction and accepted service/cable/push loads'],
                restrictions='No CAD edited, actual strength inferred, proof-load specified, contact made or physical test performed. Equal stiffness is conditional, not assured conservative. Existing isolation/restart requirements unchanged.')


def main():
    r=calculate();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'MECHANICAL_REQUIREMENTS.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    lines=['# Mechanical batch result — current R03M','',
           '**Digital requirement calculations completed; physical build release remains OPEN.**','',
           '## What was actually solved','',
           'Saved CAD mesh independently confirms both filter stop gaps are **43 mm**: 40 mm filter proxy plus 3 mm installed gasket. Each inner sleeve is **36 mm**, leaving a 7 mm stack offset. This is a dimension extraction, not a delivered-filter measurement.','',
           'The new interval solver establishes whether ONE fixed stop can cover every supplied filter/gasket/flatness tolerance. It also returns the required sleeve length if a robust window exists. No new CAD branch was created.','',
           '| Assumed case | Required nominal gap, mm | Fixed stop possible? | Candidate sleeve, mm |',
           '|---|---:|---|---:|']
    for s in r['seal_scenarios']:
        a=s['result'];sl=s['candidate_sleeve_mm']
        lines.append(f"| {s['id']} | {a['nominal_gap_lower_mm']:.2f} to {a['nominal_gap_upper_mm']:.2f} | {'Yes, for these assumptions only' if a['robust_fixed_stop_possible'] else 'NO'} | {sl:.2f} |" if sl is not None else f"| {s['id']} | {a['nominal_gap_lower_mm']:.2f} to {a['nominal_gap_upper_mm']:.2f} | NO | — |")
    lines+=['','**Do not manufacture these candidate sleeves.** The illustrative 20–40% compression bounds are not a supplier recommendation. With broad 39–41 mm filters, no fixed stop satisfies that illustrative range. Individually matched measured parts may admit a narrow window, but actual gasket limits must replace these assumptions first. Tightening more is not a valid substitute: gasket force and filter frame strength remain unknown.','',
            '## Cabinet joint demand, not capacity','',
            'Four actual groups of eight cabinet through-bolts were extracted. Loads are distributed using a linear equal-stiffness in-plane model, with no friction credit. All forces and moments are recovered by explicit equilibrium tests. In the illustrative 30 N vertical / 100 mm horizontal-offset case:','']
    for group,data in r['cabinet_groups'].items():
        peak=data['assumed_group_load_cases'][-1]['result']['peak_resultant_N']
        lines.append(f'- `{group}`: {data["bolt_count"]} bolts; peak calculated in-plane demand **{peak:.3f} N/bolt**.')
    lines+=['','These are not accepted service/test loads or capacity ratings. The model omits out-of-plane prying, panel bending/racking, wood bearing/edge breakout, screw withdrawal, joint compliance and clamps. The four groups cannot be summed as if they share load equally. Top/base wood screws remain unsuitable as an assumed lifting path; never lift by the lid.','',
            f'Exact modeled gasket ring area: **{r["cad_gasket_contact_area_mm2"]:.1f} mm²** per filter. Total idealized clamp force = supplier compression stress (MPa) × this contact area (mm²). The stress and resulting force are intentionally **UNKNOWN**; filter airflow pressure does not define gasket closing force.','',
            '## Remaining exact evidence','']
    lines+=['- '+x for x in r['physical_release_open']]
    lines+=['','Actual perforated guard/weld/attachment/probe qualification is still open. Existing solid-strip sensitivity is not a perforated guard proof and has not been promoted to one. No restart/isolation requirement was weakened. Physical prototypes: **0**.','',
            '## Reproduce / review','',
            '`python scripts/analysis/d01_mechanical_release_batch.py`','',
            '`python scripts/analysis/test_d01_mechanical_release_batch.py`','',
            'Standard library only, repository or packaged engineering root. JSON records exact input hashes, extracted coordinates, conditional force vectors and unresolved inputs. Tests are synthetic/arithmetic—not physical. Original R03M native CAD, DXFs and historical evidence are unchanged.']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Original section diagram from extracted CAD planes; not copied OEM media.
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="600" viewBox="0 0 1100 600">
<rect width="1100" height="600" fill="#f3f7fc"/>
<g font-family="Arial,sans-serif" fill="#17304b">
<text x="45" y="50" font-size="26" font-weight="bold">R03M filter closing stack — actual saved CAD</text>
<text x="45" y="80" font-size="17">REVIEW ONLY • model envelopes, not measured parts • not a fabrication setting</text>
<rect x="125" y="170" width="90" height="155" fill="#8ea4b7"/>
<rect x="215" y="170" width="400" height="155" fill="#bbd8f5"/>
<rect x="615" y="170" width="30" height="155" fill="#eead60"/>
<rect x="645" y="170" width="90" height="155" fill="#8ea4b7"/>
<text x="125" y="151" font-size="16">Retainer</text>
<text x="320" y="235" font-size="23">Filter proxy: 40 mm</text>
<text x="654" y="151" font-size="16">Reducer</text>
<path d="M630 280 L860 280" stroke="#17304b" stroke-width="2"/>
<text x="770" y="221" font-size="17">Installed gasket</text>
<text x="770" y="249" font-size="17">3 mm in CAD</text>
<path d="M215 335 V385 M645 335 V385 M215 368 H645" stroke="#17304b" fill="none" stroke-width="2"/>
<text x="294" y="399" font-size="21">Fixed closing gap: 43 mm</text>
<text x="142" y="350" font-size="14">y = -55</text>
<text x="650" y="350" font-size="14">y = -12</text>
<text x="45" y="451" font-size="18">Gap = measured filter thickness + compressed gasket thickness</text>
<text x="45" y="482" font-size="18">Current sleeve 36 mm + fixed stack offset 7 mm = gap 43 mm</text>
<text x="45" y="523" font-size="18" fill="#ad4b22">Do not assume 43 mm seals every delivered filter: broad tolerance cases fail.</text>
<text x="45" y="553" font-size="16">Run the interval solver with actual gasket limits, filter dimensions and flatness before selecting stops.</text>
</g></svg>'''
    (OUT/'FILTER_STACK_SECTION.svg').write_text(svg,encoding='utf-8')
    print(json.dumps(dict(front=r['cad_filter_stacks']['Front'],groups=len(r['cabinet_groups']),
                         fan_screws=r['cad_fan_screw_count'],native_sha256=r['input_sha256']['D01_R03M_ASSEMBLY.FCStd']),indent=2))


if __name__=='__main__':
    main()
