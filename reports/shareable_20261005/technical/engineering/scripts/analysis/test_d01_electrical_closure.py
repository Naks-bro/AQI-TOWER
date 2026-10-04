"""Analytic/synthetic checks ONLY. Never records physical commissioning PASS."""
import unittest
from d01_electrical_closure import demand, copper_loop_drop, build


class PowerTests(unittest.TestCase):
    def test_published_current_arithmetic(self):
        self.assertAlmostEqual(demand(1,0)['total_A'],1.4)
        self.assertAlmostEqual(demand(1,0)['total_W'],16.8)
        self.assertAlmostEqual(demand(1,0)['arithmetic_margin_A'],.6)

    def test_auxiliary_reduces_headroom(self):
        self.assertAlmostEqual(demand(1,.1)['arithmetic_margin_A'],.5)
        self.assertAlmostEqual(demand(1,.1)['maximum_multiplier_at_assumed_auxiliary'],1.9/1.4)

    def test_continuous_limit_boundary(self):
        self.assertFalse(demand(2/1.4,0)['exceeds_catalogue_continuous_limit'])
        self.assertTrue(demand(1.5,0)['exceeds_catalogue_continuous_limit'])

    def test_larger_supply_cannot_remove_hub_limit(self):
        row=demand(2,0,supply_A=5)
        self.assertEqual(row['governing_current_limit_A'],2)
        self.assertTrue(row['exceeds_catalogue_continuous_limit'])

    def test_drop_known_case(self):
        self.assertAlmostEqual(copper_loop_drop(1.4,1,.5)['drop_V'],.098)

    def test_drop_scales(self):
        base=copper_loop_drop(1,1,.5)
        self.assertAlmostEqual(copper_loop_drop(2,1,.5)['drop_V'],2*base['drop_V'])
        self.assertAlmostEqual(copper_loop_drop(2,1,.5)['conductor_loss_W'],4*base['conductor_loss_W'])
        self.assertAlmostEqual(copper_loop_drop(1,1,1)['drop_V'],base['drop_V']/2)
        self.assertGreater(copper_loop_drop(1,1,.5,40)['drop_V'],base['drop_V'])

    def test_no_load_zero_drop(self):
        self.assertEqual(copper_loop_drop(0,1,.5)['drop_V'],0)

    def test_bad_load_inputs(self):
        for k,a in [(0,0),(1,-1),(float('nan'),0),(float('inf'),0)]:
            with self.assertRaises(ValueError): demand(k,a)

    def test_bad_wire_inputs(self):
        for i,l,s,t in [(-1,1,.5,20),(1,-1,.5,20),(1,1,0,20),(1,1,.5,100),(1,1,.5,float('nan'))]:
            with self.assertRaises(ValueError): copper_loop_drop(i,l,s,t)

    def test_no_synthetic_release(self):
        report=build()
        self.assertEqual(len(report['load_scenarios']),20)
        self.assertEqual(len(report['voltage_drop_scenarios']),36)
        for k in ('energization','procurement','fuse_selected','wire_selected','safety_function_implemented'):
            self.assertFalse(report['release'][k])
        self.assertTrue(all(v is None for v in report['unresolved'].values()))
        self.assertEqual(report['release']['physical_tests'],0)


if __name__ == '__main__':
    unittest.main()
