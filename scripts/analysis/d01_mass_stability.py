"""R03M mass moments and nominal foot support. Assumptions, NOT safety release.

Run from repository or packaged engineering root. No third-party dependencies.
Actual complete mass is intentionally not calculated from missing component data.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/prototype_d01/mechanical_package'
OEM = 'https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf'


def hull(points):
    points = sorted(set(points))
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        result = []
        for p in seq:
            while len(result) > 1 and cross(result[-2], result[-1], p) <= 0:
                result.pop()
            result.append(p)
        return result
    return half(points)[:-1] + half(points[::-1])[:-1]


def edge_screen(mass, centre, polygon, force_height):
    """Force normal/outward to each CCW edge, on level floor, N and mm.

    Incline angle is geometric tipping onset with downslope normal to that edge.
    No friction, deformation, dynamic load, anchoring or safety factor included.
    """
    if mass <= 0 or force_height <= 0 or centre[2] <= 0 or len(polygon) < 3:
        raise ValueError('Positive mass, force height, CG height and polygon required')
    if not all(math.isfinite(v) for v in [mass, force_height, *centre]):
        raise ValueError('Finite inputs required')
    result = []
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        margin = (dx*(centre[1]-a[1])-dy*(centre[0]-a[0]))/length
        result.append(dict(edge_mm=[a, b], outward_direction_xy=[dy/length, -dx/length],
                           margin_mm=margin, static_tip_force_N=mass*9.81*margin/force_height,
                           incline_onset_deg=math.degrees(math.atan2(margin, centre[2]))))
    return result


def moments(rows):
    total = sum(r['mass_kg'] for r in rows)
    return total, [sum(r['mass_kg']*r['centre_mm'][k] for r in rows)/total for k in range(3)]


def circles(path):
    lines = path.read_text().splitlines()
    pairs = list(zip(lines[::2], lines[1::2]))
    entities, current = [], None
    for code, value in pairs + [('0', 'EOF')]:
        if code.strip() == '0':
            if current and current.get('type') == 'CIRCLE':
                entities.append(current)
            current = {'type': value}
        elif current is not None:
            current[code.strip()] = value
    return [(float(c['10']), float(c['20']), float(c['40'])) for c in entities if c.get('8') == 'HOLES']


def calculate():
    inventory = json.loads((OUT/'part_inventory.json').read_text())
    mesh = json.loads((OUT/'cad_mesh.json').read_text())
    pattern = circles(OUT/'panel_DXF_REVIEW_ONLY/G_FACE.dxf')
    removed_volume = sum(math.pi*r*r for x, y, r in pattern)  # 1 mm sheet
    removed_xy = [sum(math.pi*r*r*p[k] for p in pattern for r in [p[2]])/removed_volume for k in (0, 1)]
    feet = [p for p in mesh if p['name'].startswith('M08_Foot_')]
    assert len(feet) == 4
    support = hull([tuple(v[:2]) for p in feet for v in p['vertices'] if abs(v[2]) < 1e-7])
    rows, unknown = [], []
    for p in inventory:
        name = p['id']
        rho = 650 if p['kind'] == 'panel' else 600 if name.startswith('M07_') else 7850 if p['kind'] in ('hardware', 'guard') or name.startswith('A07_') else None
        if name.startswith('F02_P14_Max_'):
            rows.append(dict(id=name, mass_kg=.245, centre_mm=p['centre_mm'],
                             basis='OEM net mass; CAD geometric centroid ASSUMED as mass location'))
        elif rho is None:
            unknown.append(name)
        else:
            mass = p['volume_mm3']*1e-9*rho
            rows.append(dict(id=name, mass_kg=mass, centre_mm=p['centre_mm'], basis=f'ASSUMED density {rho} kg/m3; nominal CAD volume'))
            if name in ('G10_Outer_fabricated_guard', 'G10_Inner_fabricated_guard'):
                z = 630.5 if 'Outer' in name else 530.5
                rows.append(dict(id=name+'_DXF_removed_holes', mass_kg=-removed_volume*1e-9*rho,
                                 centre_mm=[115+removed_xy[0], 20+removed_xy[1], z],
                                 basis='Proposed DXF holes subtracted; face placement from build_d01.py'))
    mass, centre = moments(rows)
    inputs = ['part_inventory.json', 'cad_mesh.json', 'panel_DXF_REVIEW_ONLY/G_FACE.dxf', 'D01_R03M_ASSEMBLY.FCStd']
    return dict(status='PARTIAL ASSUMED MASS ONLY / NO BUILD OR STABILITY RELEASE',
                sources_sha256={p: hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in inputs},
                fan_source=dict(url=OEM, accessed='2026-10-05', sku='ACFAN00287A', net_mass_kg=.245,
                                ambient_temperature_C=[0, 40], note='OEM specification, NOT mass measured on delivered fan'),
                guard_holes=dict(count_per_face=len(pattern), removed_volume_per_face_mm3=removed_volume,
                                 local_area_centroid_mm=removed_xy, removed_assumed_mass_both_kg=2*removed_volume*1e-9*7850),
                nominal_support_polygon_mm=support, partial_mass_kg=mass, partial_centroid_mm=centre,
                unknown_mass_objects=unknown, mass_rows=rows,
                partial_only_edge_diagnostics=edge_screen(mass, centre, support, 631),
                whole_device_mass_kg=None, whole_device_centroid_mm=None,
                limits='Nominal foot contact only; actual friction, compression, floor contact and unevenness unknown. Partial CG and tipping numbers do NOT describe the complete device. Missing masses/locations, grades, joints, real guards and measured assembly required. No impact, cable pull, service-removal qualification, sliding test or safety factor. OEM 0-40 C is not outdoor/rain suitability.')


def main():
    report = calculate()
    (OUT/'mass_stability_review.json').write_text(json.dumps(report, indent=2)+'\n')
    m, c = report['partial_mass_kg'], report['partial_centroid_mm']
    values = report['partial_only_edge_diagnostics']
    text = f'''# R03M mass and stability supplement — 5 October 2026

**NOT RELEASED. Physical prototypes: 0. No complete-device weight or stability rating.**

## What changed

- DETECTED: nominal CAD foot-contact hull is {report['nominal_support_polygon_mm']} mm in CAD x/y. This assumes all four feet contact a flat floor without deformation.
- DETECTED: the DXF has {report['guard_holes']['count_per_face']} holes per face. Subtracting these from the solid CAD guard proxies removes {report['guard_holes']['removed_assumed_mass_both_kg']:.3f} kg at assumed steel density7850 kg/m3. Native CAD remains unchanged and solid-faced.
- VERIFIED OEM SPECIFICATION: ARCTIC P14 Max ACFAN00287A net weight245 g each, four fans0.980 kg. Actual mass location is UNKNOWN; this screen uses the CAD geometric centroid as an ASSUMPTION. Source: [ARCTIC specification sheet]({OEM}), accessed5 October2026.
- ASSUMED: panel650, cleat600 and metal7850 kg/m3. These are not confirmed material grades or delivered component weights.
- RESULT: corrected partial modeled mass plus specified fan mass is **{m:.3f} kg**; partial centroid **({c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f}) mm**. This is not a whole-device estimate or guaranteed lower bound.
- UNKNOWN: {len(report['unknown_mass_objects'])} modeled objects still lack usable mass information, including filters, feet, seals and control/cable reservations. Unmodeled finishes, real wiring and fabrication variation are also excluded.

## Useful warning, not a pass

For this partial assumed assembly ONLY, outward horizontal force at631 mm above the nominal floor gives a weakest-edge static tipping balance of **{min(v['static_tip_force_N'] for v in values):.1f} N**. The partial geometry's weakest downslope tipping angle is **{min(v['incline_onset_deg'] for v in values):.1f} degrees**. Do not use either number as a finished-device limit: the actual mass distribution is not established. Sliding may happen first; friction is unknown. This is not a prescribed safety test load.

RECOMMENDATION: keep the first demonstrator indoors on a controlled flat floor, isolated from casual pushing and cable trip hazards. Do not call it suitable for public/outdoor installation. Anti-tip attachment or a broader support concept requires an assessed substrate, fixing loads and structural design, not an arbitrary ballast choice.

The same OEM sheet specifies0–40 C operating ambient. This is a limitation for eventual hot outdoor use; it does not establish weather sealing, solar-heated enclosure temperature or vandal resistance.

## Reproduce and close the gap

Run `python scripts/analysis/d01_mass_stability.py` and `python scripts/analysis/test_d01_mass_stability.py` from repository or packaged engineering root. JSON contains exact input hashes, signed hole-removal mass rows and each directional edge result. Historical `mechanical_screen.json` is preserved; its solid-face subtotal is superseded only for this corrected partial mass calculation.

To calculate a real full-device CG: record net installed mass and mass location for every omitted item, confirm selected material density/finished dimensions, include wiring/finishes and service configurations, and weigh the assembled device. Then assess joints, actual foot contact/friction, push/cable loads, floor/incline and filter-removal scenarios with qualified mechanical review. No build release is granted by these arithmetic checks.
'''
    (OUT/'MASS_STABILITY_REVIEW.md').write_text(text, encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('partial_mass_kg', 'partial_centroid_mm', 'guard_holes', 'nominal_support_polygon_mm', 'whole_device_mass_kg')}, indent=2))


if __name__ == '__main__':
    main()
