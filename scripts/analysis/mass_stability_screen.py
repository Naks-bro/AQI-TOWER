"""Partial material inventory and illustrative static moments; no safety approval."""
import csv
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
DENSITIES = {'steel_assumed': 7850, 'aluminium_assumed': 2700}
G = 9.81


def mass_kg(volume_mm3, density_kg_m3):
    if not all(math.isfinite(x) for x in (volume_mm3, density_kg_m3)):
        raise ValueError('Non-finite material input')
    if volume_mm3 < 0 or density_kg_m3 <= 0:
        raise ValueError('Invalid volume/density')
    return volume_mm3 * 1e-9 * density_kg_m3


def aggregate(parts, density):
    masses = [mass_kg(p['volume_mm3'], density) for p in parts]
    total = sum(masses)
    if total <= 0:
        raise ValueError('No positive material inventory')
    centre = [sum(m*p['geometric_centroid_mm'][i] for m, p in zip(masses, parts))/total
              for i in range(3)]
    return {'partial_material_mass_kg': total,
            'partial_material_centroid_mm': centre,
            'whole_device_mass_kg': None, 'whole_device_centre_of_gravity_mm': None}


def moments(mass, edge_distance, force, height):
    values = (mass, edge_distance, force, height)
    if any(x is None or not math.isfinite(x) or x < 0 for x in values):
        raise ValueError('Actual unknown inputs must not be treated as zero')
    if mass == 0 or edge_distance == 0:
        raise ValueError('Positive mass/support distance required')
    return {'restoring_Nm': mass*G*edge_distance, 'overturning_Nm': force*height}


def wind_example(speed, diameter=.954, height=2.215, rho=1.2, cd=1.2):
    if speed < 0 or min(diameter, height, rho, cd) <= 0:
        raise ValueError('Invalid wind example inputs')
    force = .5*rho*speed**2*cd*diameter*height
    return {'speed_m_s_ASSUMED': speed, 'force_N': force,
            'overturning_Nm': force*height/2}


def screen():
    inventory = json.loads((ROOT/'results/fan_selection/material_inventory.json').read_text(encoding='utf-8'))
    parts = inventory['parts']
    scenarios = {name: aggregate(parts, rho) for name, rho in DENSITIES.items()}
    rows = [{'part': p['part'], 'volume_mm3': p['volume_mm3'],
             **{name+'_kg': mass_kg(p['volume_mm3'], rho) for name, rho in DENSITIES.items()}}
            for p in parts]
    return {
        'status': 'PARTIAL MASS AND ILLUSTRATIVE MOMENTS ONLY; NOT STRUCTURAL RELEASE',
        'densities_kg_m3_ASSUMED': DENSITIES, 'source_sha256': inventory['source_sha256'],
        'parts': rows, 'material_scenarios_same_geometry': scenarios,
        'fan_candidate_catalogue_mass_kg': 14,
        'fan_note': 'S&P TD2000/315 candidate, not selected; actual mass centre unknown',
        'missing_mass_items': inventory['missing'],
        'actual_tipping_assessment': 'UNKNOWN: support polygon, complete masses/CG, loads and factors missing',
        'example_only_mass_100kg_edge_distance_0_4m_push_200N_at_1_5m': moments(100, .4, 200, 1.5),
        'wind_examples_NOT_SITE_DESIGN': [wind_example(v) for v in (10, 20, 30)],
        'wind_inputs_ASSUMED': {'diameter_m': .954, 'height_m': 2.215, 'rho_kg_m3': 1.2,
                               'Cd': 1.2, 'load_height_m': 2.215/2},
        'limitations': ['Mass scenarios do not approve alloy, gauge, plate spans or joints',
                        'No full-solid component allowance is assigned metal density',
                        'No actual tipping PASS/FAIL or anchor, weld, bolt or member sizing',
                        'Uniform wind toy omits site gust, terrain, dynamics and applicable code factors',
                        'Lighter material also reduces unanchored restoring weight; reassess support',
                        'Independent M04 study is not an assembled OEM installation']}


class Tests(unittest.TestCase):
    def test_units(self):
        self.assertAlmostEqual(mass_kg(1e9, 7850), 7850)

    def test_centroid(self):
        result = aggregate([{'volume_mm3': 1e6, 'geometric_centroid_mm': [0, 0, 100]},
                            {'volume_mm3': 3e6, 'geometric_centroid_mm': [0, 0, 300]}], 7850)
        self.assertAlmostEqual(result['partial_material_centroid_mm'][2], 250)
        self.assertIsNone(result['whole_device_mass_kg'])

    def test_invalid(self):
        for volume, density in ((-1, 7850), (1, 0), (float('nan'), 7850)):
            with self.assertRaises(ValueError):
                mass_kg(volume, density)

    def test_moments(self):
        result = moments(100, .4, 200, 1.5)
        self.assertAlmostEqual(result['restoring_Nm'], 392.4)
        self.assertAlmostEqual(result['overturning_Nm'], 300)

    def test_unknown_blocks(self):
        with self.assertRaises(ValueError):
            moments(None, .4, 200, 1.5)

    def test_wind_square_law(self):
        self.assertAlmostEqual(wind_example(20)['force_N'], 4*wind_example(10)['force_N'])


if __name__ == '__main__':
    output = screen()
    folder = ROOT/'results/fan_selection'
    (folder/'mass_stability_screen.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    with (folder/'material_mass_screen.csv').open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(output['parts'][0]))
        writer.writeheader()
        writer.writerows(output['parts'])
    print(json.dumps(output['material_scenarios_same_geometry'], indent=2))
