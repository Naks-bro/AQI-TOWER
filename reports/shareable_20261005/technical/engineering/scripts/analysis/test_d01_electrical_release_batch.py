"""Analytic/synthetic tests only, no physical electrical acceptance."""
import math
import unittest
from d01_electrical_release_batch import power_screen, copper_screen, input_screen


class ElectricalScreens(unittest.TestCase):
    def test_nominal(self):
        s=power_screen(); self.assertAlmostEqual(s['source_total_A'],47/30)
        self.assertAlmostEqual(s['source_margin_A'],13/30)
        self.assertAlmostEqual(s['source_multiplier_ceiling'],55/42)
    def test_auxiliary(self):
        self.assertAlmostEqual(power_screen(auxiliary_A=.1)['source_multiplier_ceiling'],26/21)
    def test_startup_not_proved(self):
        self.assertFalse(power_screen(multiplier=1.4)['within_source_continuous_screen'])
        self.assertTrue(power_screen(multiplier=1.4)['within_fan_path_continuous_screen'])
        self.assertFalse(power_screen()['startup_approved'])
    def test_zero_and_loop(self):
        self.assertEqual(copper_screen(0,1,1)['drop_V'],0)
        self.assertAlmostEqual(copper_screen(1,.5,2)['drop_V'],.14)
    def test_heat_and_contacts(self):
        self.assertGreater(copper_screen(1,.5,2,60)['drop_V'],copper_screen(1,.5,2,20)['drop_V'])
        self.assertAlmostEqual(copper_screen(0,1,2,contacts_total_ohm=.1)['drop_V'],.2)
    def test_input(self):
        self.assertAlmostEqual(input_screen()['nominal_input_mA'],12000/8900)
        self.assertAlmostEqual(input_screen()['high_threshold_margin_V'],5.4)
        self.assertFalse(input_screen()['minimum_contact_load_approved'])
    def test_input_series_monotonic(self):
        self.assertLess(input_screen(series_ohm=100)['input_V'],input_screen()['input_V'])
    def test_invalid(self):
        for call in (lambda:power_screen(multiplier=-1),lambda:power_screen(auxiliary_A=math.nan),
                     lambda:power_screen(voltage_V=0),lambda:copper_screen(1,0,1),
                     lambda:copper_screen(1,1,1,temperature_C=math.inf),lambda:input_screen(impedance_ohm=0)):
            with self.assertRaises(ValueError):call()


if __name__=='__main__': unittest.main()
