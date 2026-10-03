"""Explicit loss-coefficient sensitivity and fan static/total pressure accounting."""
import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
RHO=1.2


def velocity_pressure(flow_m3h,area_m2):
    if flow_m3h<0 or area_m2<=0:
        raise ValueError('Invalid flow/area')
    velocity=flow_m3h/3600/area_m2
    return .5*RHO*velocity**2


def static_requirement(internal_total_losses,terminal_velocity_pressure,fan_outlet_velocity_pressure):
    # Ambient intake -> discharge plane; kinetic energy at terminal handled separately.
    return internal_total_losses+terminal_velocity_pressure-fan_outlet_velocity_pressure


def screen(q=1300):
    d=.315; duct_area=math.pi*d*d/4; intake_area=8*.160*.140*.7
    pv_duct=velocity_pressure(q,duct_area); pv_intake=velocity_pressure(q,intake_area)
    specs=[('intake_entry_and_guard',3,8,pv_intake,'K, intake passage velocity'),
           ('square_to_round_transition',.1,.5,pv_duct,'K, 315mm throat velocity'),
           ('outlet_guard',1,3,pv_duct,'K, gross duct velocity; must obtain actual guard curve'),
           ('joints_and_connection',.1,.5,pv_duct,'K, duct velocity'),
           ('fan_system_effect_equivalent',0,2,pv_duct,'ASSUMED equivalent K, not a verified upper bound')]
    rows=[{'component':name,'low_input':low,'high_input':high,'reference':ref,
           'low_pressure_Pa':round(low*pv,3),'high_pressure_Pa':round(high*pv,3)}
          for name,low,high,pv,ref in specs]
    length=.010+.200
    rows.append({'component':'straight_round_neck_and_outlet','low_input':.018,'high_input':.035,
                 'reference':'ASSUMED Darcy f; f*L/D*velocity pressure; actual roughness/Re unknown',
                 'low_pressure_Pa':round(.018*length/d*pv_duct,3),
                 'high_pressure_Pa':round(.035*length/d*pv_duct,3)})
    low=sum(r['low_pressure_Pa'] for r in rows); high=sum(r['high_pressure_Pa'] for r in rows)
    clean=(111.2+25)*q/1332; loaded=(111.2*2+80)*q/1332
    return {'status':'COEFFICIENT SENSITIVITY ONLY — NOT MEASURED LOSS OR DESIGN BOUNDS',
            'flow_m3h_assumed':q,'air_density_kg_m3_assumed':RHO,
            'duct_clear_diameter_m_assumed':d,'intake_free_area_fraction_assumed':.7,
            'duct_velocity_m_s':round(q/3600/duct_area,3),'duct_velocity_pressure_Pa':round(pv_duct,3),
            'components':rows,'hardware_scenario_range_Pa':[round(low,2),round(high,2)],
            'same_area_terminal_vs_fan_outlet_static_duty_clean_Pa':[round(clean+low,2),round(clean+high,2)],
            'same_area_terminal_vs_fan_outlet_static_duty_loaded_Pa':[round(loaded+low,2),round(loaded+high,2)],
            'limitations':['All coefficients and friction factors are scenario inputs, not measured or cited fitting values',
                           'No bends/carbon/silencer/weather louvre in this branch; add if introduced',
                           '315mm actual fan outlet area not verified; no OEM pressure-basis match yet',
                           'Additional external backpressure and nonuniform flow not bounded',
                           'Loaded factors are assumptions; no approved maintenance threshold']}


class Tests(unittest.TestCase):
    def test_same_area_static_cancels_terminal_kinetic(self):
        self.assertEqual(static_requirement(150,12,12),150)
    def test_reduced_terminal_area_raises_static_requirement(self):
        self.assertEqual(static_requirement(150,30,12),168)
    def test_velocity_pressure_scales_quadratic(self):
        self.assertAlmostEqual(velocity_pressure(2000,.1),4*velocity_pressure(1000,.1))
    def test_smaller_area_higher_velocity_pressure(self):
        self.assertGreater(velocity_pressure(1300,.05),velocity_pressure(1300,.1))
    def test_scenario_sum(self):
        r=screen(); self.assertAlmostEqual(sum(x['low_pressure_Pa'] for x in r['components']),r['hardware_scenario_range_Pa'][0],places=2)
        self.assertGreater(r['same_area_terminal_vs_fan_outlet_static_duty_loaded_Pa'][0],r['same_area_terminal_vs_fan_outlet_static_duty_clean_Pa'][0])


if __name__=='__main__':
    if not unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful():
        raise SystemExit(1)
    r=screen(); out=ROOT/'results/fan_selection/airpath_loss_screen.json'
    out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8'); print(json.dumps(r,indent=2))
