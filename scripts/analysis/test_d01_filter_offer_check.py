"""Synthetic software fixtures only; not manufacturer or physical measurements."""
import unittest
from d01_filter_offer_check import validate,interpolate,assess
class CurveTests(unittest.TestCase):
    def test_midpoint(self):self.assertEqual(interpolate([(100,5),(200,15)],150),10)
    def test_no_low_extrapolation(self):self.assertIsNone(interpolate([(100,5),(200,15)],50))
    def test_no_high_extrapolation(self):self.assertIsNone(interpolate([(100,5),(200,15)],250))
    def test_endpoints(self):self.assertEqual(interpolate([(100,5),(200,15)],200),15)
    def test_single_point_rejected(self):
        with self.assertRaises(ValueError):validate([(200,15)])
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):validate([(100,5),(100,15)])
    def test_decreasing_pressure_rejected(self):
        with self.assertRaises(ValueError):validate([(100,15),(200,5)])
    def test_nonfinite_and_negative_rejected(self):
        for points in ([(0,0),(float('nan'),1)],[(0,0),(100,-1)]):
            with self.assertRaises(ValueError):validate(points)
    def test_filter_pressure_not_doubled(self):
        rows=assess([(100,5),(200,15)],[dict(each_filter_flow_m3h=150,brochure_filter_headroom_Pa=14.5,numeric_filter_headroom_Pa=14.7)])
        self.assertEqual(rows[0]['supplied_curve_pressure_Pa'],10)
        self.assertEqual(rows[0]['remaining_model_margin_Pa'],4.5)
        self.assertEqual(rows[0]['total_flow_m3h'],300)
    def test_high_pressure_flagged(self):
        rows=assess([(100,20),(200,30)],[dict(each_filter_flow_m3h=150,brochure_filter_headroom_Pa=14.5,numeric_filter_headroom_Pa=14.7)])
        self.assertEqual(rows[0]['screening_status'],'EXCEEDS_MODEL_ALLOWANCE')
if __name__=='__main__':unittest.main()
