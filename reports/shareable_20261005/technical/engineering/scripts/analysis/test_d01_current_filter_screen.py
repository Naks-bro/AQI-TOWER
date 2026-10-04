"""Synthetic checks only. These fixtures are never published as physical evidence."""
import math
import unittest
import d01_current_filter_screen as f
import d01_validation as v


class FilterScreenTests(unittest.TestCase):
    def test_current_geometry_budget(self):
        budget=v.pressure_rows()
        case=next(r for r in budget['rows'] if r['total_m3h']==300 and r['reducer_K']==1)
        self.assertAlmostEqual(case['filter_allowance_Pa'],14.316071817116585)
        rows=f.assess([(100,10),(200,20)],budget)
        row=next(r for r in rows if r['total_flow_m3h']==300 and r['reducer_K']==1)
        self.assertEqual(row['supplied_per_filter_pressure_Pa'],15)
        self.assertAlmostEqual(row['remaining_model_margin_Pa'],-.683928182883415)
        self.assertEqual(row['status'],'NO_POSITIVE_MODEL_MARGIN')

    def test_no_extrapolation(self):
        rows=f.assess([(140,10),(160,12)],v.pressure_rows())
        self.assertEqual(sum(r['status']=='OUTSIDE_CURVE_RANGE' for r in rows),12)

    def test_zero_margin_not_approval(self):
        budget={'rows':[dict(total_m3h=300,per_filter_m3h=150,reducer_K=1,
                             fan_Pa=30,nonfilter_Pa=20,filter_allowance_Pa=10)]}
        self.assertEqual(f.assess([(100,10),(200,10)],budget)[0]['status'],'NO_POSITIVE_MODEL_MARGIN')

    def test_curve_rejections(self):
        for points in ([(100,1)],[(100,1),(100,2)],[(200,1),(100,2)],
                       [(100,2),(200,1)],[(100,-1),(200,2)],
                       [(100,math.nan),(200,2)],[(100,1),(math.inf,2)]):
            with self.subTest(points=points),self.assertRaises(ValueError):
                f.assess(points,v.pressure_rows())

    def test_equal_parallel_branches(self):
        rows=f.assess([(0,0),(200,10)],v.pressure_rows())
        self.assertTrue(all(r['total_flow_m3h']==2*r['per_filter_flow_m3h'] for r in rows))
        self.assertEqual(len(rows),15)


if __name__=='__main__':
    unittest.main()
