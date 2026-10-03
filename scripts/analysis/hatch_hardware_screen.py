"""M05 illustrative closure screening; no latch sizing or seal certification."""
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


def positive(*values):
    if any(not math.isfinite(v) or v <= 0 for v in values):
        raise ValueError('Inputs must be finite and positive')


def ring_area(outer_w, outer_h, inner_w, inner_h):
    positive(outer_w, outer_h, inner_w, inner_h)
    if inner_w >= outer_w or inner_h >= outer_h:
        raise ValueError('Inner dimensions must be smaller')
    return (outer_w * outer_h - inner_w * inner_h) / 1e6


def compression(free_mm, gap_mm):
    positive(free_mm, gap_mm)
    return max(0, (free_mm - gap_mm) / free_mm)


def force_at_test_strain(area_m2, stress_kpa, strain):
    positive(area_m2, stress_kpa)
    if not math.isclose(strain, 0.25, abs_tol=1e-9):
        raise ValueError('Published stress is only used at 25% test deflection')
    return area_m2 * stress_kpa * 1000


def calculate():
    area = ring_area(665, 330, 645, 310)
    return {
        'status': 'ILLUSTRATIVE SCREENING ONLY; NO HARDWARE SELECTED',
        'geometry_basis': 'M05 assumed rectangular full-contact gasket ring',
        'gasket_area_m2': area,
        'assumed_door_pressure_Pa': 500,
        'door_pressure_force_N': 500 * .645 * .310,
        'gasket_example': {
            'source': 'Rogers 17-007, 0724-PDF, PORON 4701-40, 240 kg/m3 grade',
            'test_strain': .25, 'test_speed_cm_min': .51,
            'force_range_N': [force_at_test_strain(area, s, .25) for s in (27, 76)],
            'typical_force_N': force_at_test_strain(area, 41, .25),
            'nominal_free_mm': 3.18, 'thickness_tolerance_fraction': .10,
            'existing_assumed_gap_mm': 3,
            'nominal_compression_existing_gap': compression(3.18, 3),
            'thinnest_example_has_contact_at_3mm': 3.18 * .9 >= 3,
            'nominal_25pct_gap_mm': 3.18 * .75,
            'fixed_gap_tolerance_compression_range': [compression(t, 3.18 * .75) for t in (3.18 * .9, 3.18 * 1.1)],
            'limitations': 'Uniform coupon-stress extrapolation, not actual installed preload; no stress extrapolation outside 25%. No material selection.'
        },
        'cutout_screen': {
            'assumed_land_mm': 15,
            'C5_90_min_short_cutout_mm': 34,
            'C5_71_min_short_cutout_mm': 24,
            'either_cutout_fits_wholly_in_15mm_land': False,
            'scope': 'Rim-only placement, not a whole-panel or full operating-sweep assessment'
        },
        'required_latch_count': None,
        'closing_force_rating': None,
        'physical_tests': 0
    }


class HatchHardwareTests(unittest.TestCase):
    def test_area_units(self):
        self.assertAlmostEqual(ring_area(665, 330, 645, 310), .0195)

    def test_force_units(self):
        self.assertAlmostEqual(force_at_test_strain(.0195, 27, .25), 526.5)
        self.assertAlmostEqual(force_at_test_strain(.0195, 76, .25), 1482)

    def test_wrong_strain_rejected(self):
        with self.assertRaises(ValueError):
            force_at_test_strain(.0195, 41, .1)

    def test_no_contact(self):
        self.assertEqual(compression(2.862, 3), 0)

    def test_tolerance(self):
        r = calculate()['gasket_example']['fixed_gap_tolerance_compression_range']
        self.assertAlmostEqual(r[0], 1/6)
        self.assertAlmostEqual(r[1], 7/22)

    def test_invalid_geometry_and_no_selection(self):
        with self.assertRaises(ValueError):
            ring_area(1, 1, 2, 2)
        with self.assertRaises(ValueError):
            compression(float('nan'), 3)
        self.assertIsNone(calculate()['required_latch_count'])


if __name__ == '__main__':
    output = ROOT / 'results/fan_selection/hatch_hardware_screen.json'
    output.write_text(json.dumps(calculate(), indent=2) + '\n', encoding='utf-8')
    print(output)
