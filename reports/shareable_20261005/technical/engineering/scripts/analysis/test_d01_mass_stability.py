"""Analytic/synthetic checks, not physical test evidence."""
import math
import unittest
from d01_mass_stability import hull, moments, edge_screen, calculate


class StabilityTests(unittest.TestCase):
    def test_rectangle_and_inside_points(self):
        self.assertEqual(hull([(0,0),(100,0),(100,100),(0,100),(50,50)]), [(0,0),(100,0),(100,100),(0,100)])

    def test_level_force_and_incline(self):
        rows = edge_screen(10, [50,50,100], hull([(0,0),(100,0),(100,100),(0,100)]), 200)
        for row in rows:
            self.assertAlmostEqual(row['static_tip_force_N'], 24.525)
            self.assertAlmostEqual(row['incline_onset_deg'], math.degrees(math.atan(.5)))

    def test_offcentre_and_outside(self):
        poly = hull([(0,0),(100,0),(100,100),(0,100)])
        self.assertEqual(min(r['margin_mm'] for r in edge_screen(10,[50,10,100],poly,200)),10)
        self.assertLess(min(r['static_tip_force_N'] for r in edge_screen(10,[50,-10,100],poly,200)),0)

    def test_mass_moment_subtraction(self):
        m, c = moments([dict(mass_kg=2,centre_mm=[0,0,10]),dict(mass_kg=-1,centre_mm=[0,0,20])])
        self.assertEqual((m,c),(1,[0,0,0]))

    def test_invalid_inputs(self):
        poly = [(0,0),(100,0),(0,100)]
        for mass, height in [(0,100),(10,0),(float('nan'),100)]:
            with self.assertRaises(ValueError):
                edge_screen(mass,[10,10,10],poly,height)

    def test_actual_inputs_remain_partial(self):
        r = calculate()
        self.assertEqual(r['guard_holes']['count_per_face'],2822)
        self.assertEqual(r['nominal_support_polygon_mm'],[(25.0,15.0),(525.0,15.0),(525.0,345.0),(25.0,345.0)])
        self.assertIsNone(r['whole_device_mass_kg'])
        self.assertTrue(r['unknown_mass_objects'])
        self.assertAlmostEqual(r['partial_mass_kg'],12.189836490915319+.980-r['guard_holes']['removed_assumed_mass_both_kg'])
        self.assertEqual(r['sources_sha256']['D01_R03M_ASSEMBLY.FCStd'],'fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6')


if __name__ == '__main__':
    unittest.main()
