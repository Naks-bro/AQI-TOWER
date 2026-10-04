"""Rigid equal-stiffness four-contact reaction sensitivity, not a plate design."""
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
G = 9.81


def reactions(mass_kg, ex=0, ey=0, moment_x=0, moment_y=0, a=.350, b=.200, contact_area_mm2=1225):
    values = (mass_kg,ex,ey,moment_x,moment_y,a,b,contact_area_mm2)
    if any(v is None or not math.isfinite(v) for v in values):
        raise ValueError('Unknown/nonfinite loads must not be replaced with zero')
    if min(mass_kg,a,b,contact_area_mm2) <= 0:
        raise ValueError('Positive mass, half-spans and nominal area required')
    weight = mass_kg*G
    mx, my = weight*ey+moment_x, weight*ex+moment_y
    rows = []
    for sx,sy in [(1,1),(-1,1),(-1,-1),(1,-1)]:
        force = weight/4+sx*my/(4*a)+sy*mx/(4*b)
        rows.append({'x_m':sx*a,'y_m':sy*b,'reaction_N':force,
                     'nominal_compression_average_MPa':max(force,0)/contact_area_mm2})
    return {'mass_kg_ASSUMED':mass_kg,'eccentricity_m_ASSUMED':[ex,ey],
            'additional_reaction_first_moments_Nm_ASSUMED':[moment_x,moment_y],
            'weight_N':weight,'target_first_moments_Nm':[mx,my],
            'contacts':rows,'contact_only_model_valid':all(r['reaction_N']>=0 for r in rows),
            'structural_approval':'UNKNOWN: no allowable stress or joint rating established'}


def contact_overlap(dx_mm,dy_mm,side_mm=35):
    if side_mm <= 0:
        raise ValueError('Invalid contact size')
    return max(0,side_mm-abs(dx_mm))*max(0,side_mm-abs(dy_mm))


def screen():
    inv = json.loads((ROOT/'results/fan_selection/support_load_inventory.json').read_text(encoding='utf-8'))
    partial = {name:mass+inv['fan_candidate_OEM_mass_kg']
               for name,mass in inv['plane_material_totals_kg_ASSUMED_steel'].items()}
    hepa = partial['HEPA_upper_face']
    cases = {'partial_HEPA_concentric':reactions(hepa),
             'partial_prefilter_concentric':reactions(partial['prefilter_upper_face']),
             'HEPA_plus_ASSUMED_20kg_missing_components':reactions(hepa+20),
             'HEPA_plus_20kg_ASSUMED_offset_150x100mm':reactions(hepa+20,.15,.10),
             'HEPA_plus_20kg_ASSUMED_200N_lateral_at_1_2m':reactions(hepa+20,moment_x=200*(1.2-.645)),
             'HEPA_plus_20kg_ASSUMED_300N_lateral_at_1_2m':reactions(hepa+20,moment_x=300*(1.2-.645))}
    return {'status':'LOAD-TRANSFER SENSITIVITY ONLY; NO PLATE/JOINING RELEASE',
            'partial_plane_subtotals_with_candidate_fan_kg':partial,
            'subtotal_note':'Not actual load ratings or total machine weights; missing loads are NOT zero',
            'cases':cases,
            'cap_projected_alignment_examples_mm2':[
                {'dx_mm':d,'dy_mm':d,'projected_overlap_mm2':contact_overlap(d,d)} for d in (0,1,3,5)],
            'pressure_example_500Pa_HEPA_gross_face_force_N':500*.593**2,
            'assumptions':['Rigid load-distribution plane, four equal-stiffness supports',
                           'Caps nominally aligned at x +/-350 and y +/-200 mm',
                           'Plate flexibility, frame racking and joint preload ignored',
                           'Moments are demand first moments of vertical reactions; not a signed external-load specification',
                           'Negative reaction means contact-only linear model invalid; no redistribution or anchor design',
                           'Nominal force/1225 mm2 is not peak bearing, plate bending, cap or weld stress',
                           'Positive reactions do not establish whole-device tipping/sliding safety'],
            'source_sha256':inv['source_sha256_unchanged'],
            'unknowns':inv['excluded']+['material grade/allowables','actual connection stiffness and tolerance',
                                       'gasket compression and allowable seal-plane deflection']}


class Tests(unittest.TestCase):
    def test_concentric(self):
        r = reactions(100)
        self.assertTrue(all(abs(c['reaction_N']-245.25)<1e-8 for c in r['contacts']))

    def test_force_and_moment_balance(self):
        r = reactions(100,.1,.05,20,30)
        self.assertAlmostEqual(sum(c['reaction_N'] for c in r['contacts']),r['weight_N'])
        self.assertAlmostEqual(sum(c['y_m']*c['reaction_N'] for c in r['contacts']),r['target_first_moments_Nm'][0])
        self.assertAlmostEqual(sum(c['x_m']*c['reaction_N'] for c in r['contacts']),r['target_first_moments_Nm'][1])

    def test_contact_loss(self):
        self.assertFalse(reactions(50,moment_x=200)['contact_only_model_valid'])

    def test_unknown(self):
        with self.assertRaises(ValueError):
            reactions(None)

    def test_nominal_pressure_units(self):
        self.assertAlmostEqual(reactions(100)['contacts'][0]['nominal_compression_average_MPa'],245.25/1225)

    def test_alignment(self):
        self.assertEqual(contact_overlap(3,3),1024)
        self.assertEqual(contact_overlap(36,0),0)


if __name__ == '__main__':
    result = screen()
    (ROOT/'results/fan_selection/plate_load_screen.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for name,case in result['cases'].items():
        forces = [r['reaction_N'] for r in case['contacts']]
        print(name, 'mass kg',round(case['mass_kg_ASSUMED'],2),'reactions N', [round(v,1) for v in forces],
              'contact-only model valid',case['contact_only_model_valid'])
