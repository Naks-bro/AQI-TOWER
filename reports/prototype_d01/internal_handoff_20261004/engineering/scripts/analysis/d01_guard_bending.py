"""Ideal solid-strip sensitivity, NOT perforated guard strength or safety approval."""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'reports/prototype_d01/mechanical_package'


def strip(load_n, span_mm, width_mm, thickness_mm, modulus_mpa=200000):
    """Simply supported elastic rectangular strip, midpoint point force; N/mm units."""
    values = (load_n, span_mm, width_mm, thickness_mm, modulus_mpa)
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError('All inputs must be finite and positive')
    inertia = width_mm * thickness_mm**3 / 12
    moment = load_n * span_mm / 4
    deflection = load_n * span_mm**3 / (48 * modulus_mpa * inertia)
    return dict(load_N=load_n, span_mm=span_mm, width_mm=width_mm,
                thickness_mm=thickness_mm, assumed_E_MPa=modulus_mpa,
                I_mm4=inertia, elastic_deflection_mm=deflection,
                nominal_elastic_stress_MPa=moment * thickness_mm / (2 * inertia),
                deflection_to_thickness=deflection / thickness_mm,
                warning='Ideal SOLID strip, not installed perforated plate. No yield or safety assessment.')


def selftest():
    a = strip(30, 300, 300, 1)
    assert math.isclose(a['I_mm4'], 25)
    assert math.isclose(a['elastic_deflection_mm'], 3.375)
    assert math.isclose(a['nominal_elastic_stress_MPa'], 45)
    assert math.isclose(strip(60,300,300,1)['elastic_deflection_mm'], 2*3.375)
    assert math.isclose(strip(30,150,300,1)['elastic_deflection_mm'], 3.375/8)
    assert math.isclose(strip(30,300,300,2)['elastic_deflection_mm'], 3.375/8)
    assert math.isclose(strip(30,300,30,1)['elastic_deflection_mm'], 3.375*10)
    assert math.isclose(strip(30,300,300,2)['nominal_elastic_stress_MPa'], 45/4)
    count = 8
    for i in range(5):
        for invalid in (0, -1, float('nan'), float('inf')):
            args = [30,300,300,1,200000]; args[i] = invalid
            try:
                strip(*args)
            except ValueError:
                count += 1
            else:
                raise AssertionError('Invalid input accepted')
    return count


def evaluate():
    source = PACKAGE / 'guard_pattern.json'
    p = json.loads(source.read_text())
    w,h,t = p['outside_mm']
    net_area = w*h/1e6 - p['hole_area_m2']
    # 300 mm active width is known; support span is separately ASSUMED below.
    rows = [strip(f, span, width, thickness)
            for f in (10,30,60) for span in (300,150)
            for width in (30,300) for thickness in (1,1.5,2)]
    return dict(status='PARAMETRIC SENSITIVITY ONLY - NO GUARD PASS/FAIL',
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        detected=dict(face_blank_mm=p['outside_mm'], hole_count=p['holes'],
                      hole_area_m2=p['hole_area_m2'], net_face_material_area_m2=net_area),
        assumptions=dict(E_MPa=200000, density_kg_m3=7850,
                         force_N=[10,30,60], span_mm=[300,150], load_sharing_width_mm=[30,300],
                         note='Forces are sensitivity inputs, NOT regulatory proof loads. 150 mm span assumes a new effective support that is NOT designed. No material grade selected.'),
        face_mass_scenarios=[dict(thickness_mm=x, mass_each_kg=net_area*x/1000*7850)
                             for x in (1,1.5,2)],
        limitations=['Actual face is a two-way perforated plate, not a one-way solid beam.',
                     '30/300 mm load-sharing widths and support spans are assumptions, not bounds.',
                     'Do not reduce modulus by open-area fraction; this does not model hole ligaments.',
                     'Large deflection, yielding, local indentation, welds, brackets and cabinet attachments omitted.',
                     'No comparison to 22/50 mm body gaps can certify blade clearance or safe reach.',
                     'A rib changes attachment loading and obstructs airflow; no rib or thicker sheet released.'],
        source='https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf',
        source_note='American Wood Council beam formulas, Figure7; generic elastic beam equation only, not wood design values or guard certification. Checked2026-10-04.',
        equations='I=b*t^3/12; M=P*L/4; delta=P*L^3/(48*E*I); sigma=M*t/(2*I). N,mm,MPa.',
        rows=rows, synthetic_checks=selftest(), physical_tests=0)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=evaluate()
    if args.output:
        with args.output.open('x',encoding='utf-8') as f:
            json.dump(data,f,indent=2)
    print(json.dumps({'synthetic_checks':data['synthetic_checks'],
                      'scenarios':len(data['rows']), 'face_mass_scenarios':data['face_mass_scenarios'],
                      'reference_case':strip(30,300,300,1), 'physical_tests':0},indent=2))
