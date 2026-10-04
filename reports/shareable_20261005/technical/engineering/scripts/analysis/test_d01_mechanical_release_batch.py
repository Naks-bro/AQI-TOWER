"""Synthetic and saved-CAD arithmetic checks; NOT physical qualification."""
import math
import unittest
from d01_mechanical_release_batch import seal_window, compression_bounds, joint_demands, calculate


class MechanicalBatchTests(unittest.TestCase):
    def test_exact_nominal_seal(self):
        r=seal_window([40,40],[4,4],[.25,.25],0)
        self.assertEqual(r['nominal_gap_midpoint_mm'],43)
        self.assertTrue(r['robust_fixed_stop_possible'])

    def test_wide_filter_no_common_stop(self):
        self.assertFalse(seal_window([39,41],[4,4],[.2,.4],.25)['robust_fixed_stop_possible'])

    def test_matched_window_and_every_corner(self):
        r=seal_window([39.9,40.1],[3.9,4.1],[.2,.4],.1)
        self.assertAlmostEqual(r['nominal_gap_lower_mm'],42.66)
        self.assertAlmostEqual(r['nominal_gap_upper_mm'],42.92)
        for gap in (r['nominal_gap_lower_mm'],r['nominal_gap_upper_mm']):
            c=compression_bounds(gap,[39.9,40.1],[3.9,4.1],.1)
            self.assertGreaterEqual(c['min_fraction']+.0000001,.2)
            self.assertLessEqual(c['max_fraction']-.0000001,.4)

    def test_loss_of_contact_and_overclosure_not_clipped(self):
        self.assertLess(compression_bounds(45,[40,40],[4,4])['min_fraction'],0)
        self.assertGreater(compression_bounds(38,[40,40],[4,4])['max_fraction'],1)

    def test_invalid_seal(self):
        for t,f,c,e in [([41,39],[4,4],[.2,.4],0),([40,40],[0,4],[.2,.4],0),
                        ([40,40],[4,4],[.2,1],0),([40,40],[4,4],[.2,.4],-1),
                        ([40,40],[4,4],[.2,.4],math.nan)]:
            with self.assertRaises(ValueError):seal_window(t,f,c,e)

    def test_centred_direct_load(self):
        r=joint_demands([[-1,-1],[-1,1],[1,-1],[1,1]],[0,-40],0)
        self.assertEqual(r['peak_resultant_N'],10)
        self.assertEqual(r['recovered_force_N'],[0,-40])

    def test_force_and_moment_equilibrium(self):
        for moment in (-3000,0,3000):
            r=joint_demands([[0,0],[0,3],[4,0],[4,3]],[7,-30],moment)
            self.assertAlmostEqual(r['recovered_force_N'][0],7)
            self.assertAlmostEqual(r['recovered_force_N'][1],-30)
            self.assertAlmostEqual(r['recovered_moment_Nmm'],moment)

    def test_joint_translation_invariant(self):
        a=joint_demands([[0,0],[0,3],[4,0],[4,3]],[7,-30],3000)
        b=joint_demands([[10,20],[10,23],[14,20],[14,23]],[7,-30],3000)
        self.assertEqual(a['force_vectors_N'],b['force_vectors_N'])

    def test_degenerate_group_rejected(self):
        with self.assertRaises(ValueError):joint_demands([[1,1],[1,1]],[0,1],0)

    def test_saved_cad_and_unknowns(self):
        r=calculate()
        for side in r['cad_filter_stacks'].values():
            self.assertAlmostEqual(side['nominal_stop_gap_mm'],43)
            self.assertAlmostEqual(side['modeled_inner_sleeve_mm'],36)
            self.assertAlmostEqual(side['gap_minus_sleeve_mm'],7)
        self.assertEqual(r['cad_fan_screw_count'],16)
        for g in r['cabinet_groups'].values():self.assertEqual(g['bolt_count'],8)
        self.assertIsNone(r['actual_material_allowables_MPa'])
        self.assertIsNone(r['clamp_force_relationship']['installed_total_force_N'])
        self.assertEqual(r['input_sha256']['D01_R03M_ASSEMBLY.FCStd'],
                         'fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6')


if __name__=='__main__':unittest.main()
