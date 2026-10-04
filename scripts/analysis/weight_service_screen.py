"""Same-geometry density scenarios and hypothetical tolerance/envelope arithmetic."""
import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
STEEL=7850
ALUMINIUM=2700


def side_gap(opening,part,opening_shortfall=0,part_oversize=0,offset=0,coating_each_face=0):
    if min(opening,part)<=0 or min(opening_shortfall,part_oversize,offset,coating_each_face)<0:
        raise ValueError('Invalid tolerance inputs')
    return (opening-opening_shortfall-part-part_oversize)/2-offset-2*coating_each_face


def corner_clearance(shell_inner_diameter,opening,seal_land,projection,housing_side=653):
    if min(shell_inner_diameter,opening,housing_side)<=0 or min(seal_land,projection)<0:
        raise ValueError('Invalid panel envelope')
    # Flat front panel, centred about x=0; circular shell also centred, y negative.
    radius=math.hypot(opening/2+seal_land,housing_side/2+projection)
    return shell_inner_diameter/2-radius


def subtotal(parts,aluminium_groups=()):
    totals={}
    for p in parts:
        density=ALUMINIUM if p['group'] in aluminium_groups else STEEL
        totals[p['group']]=totals.get(p['group'],0)+p['volume_mm3']*1e-9*density
    return {'groups_kg':totals,'partial_material_mass_kg':sum(totals.values()),
            'complete_machine_mass_kg':None}


def screen():
    inventory=json.loads((ROOT/'results/fan_selection/housing_mass_groups.json').read_text(encoding='utf-8'))
    p=inventory['parts']
    scenarios={'all_steel_baseline':subtotal(p),
               'aluminium_cosmetic_casing_only':subtotal(p,('cosmetic_casing',)),
               'aluminium_casing_and_inner_panels':subtotal(p,('cosmetic_casing','inner_housing_panels'))}
    return {'status':'DENSITY AND ASSUMED SERVICE ENVELOPE COMPARISON; NO MATERIAL OR DIMENSION RELEASE',
            'source':inventory['source'],'sha256_unchanged':inventory['sha256_unchanged'],
            'densities_ASSUMED_kg_m3':{'steel':STEEL,'aluminium':ALUMINIUM},
            'same_geometry_material_scenarios':scenarios,
            'service_opening_examples':[
                {'opening_mm_ASSUMED':opening,'part_width_mm_ASSUMED':633,
                 'nominal_side_gap_mm':side_gap(opening,633),
                 'sensitivity_side_gap_mm':side_gap(opening,633,1,1,1,.2)} for opening in (635,645)],
            'tolerance_sensitivity_ASSUMED':{'opening_total_shortfall_mm':1,'part_total_oversize_mm':1,
                                           'lateral_offset_mm':1,'coating_each_contact_face_mm':.2},
            'flat_service_panel_corner_examples':[
                {'shell_inner_diameter_mm_ASSUMED':diameter,'opening_mm_ASSUMED':645,
                 'seal_land_each_side_mm_ASSUMED':15,'forward_projection_mm_ASSUMED':10,
                 'nominal_corner_clearance_mm':corner_clearance(diameter,645,15,10)} for diameter in (950,980)],
            'limitations':['All material scenarios preserve existing geometry; no modulus/strength/corrosion approval',
                           'Frame, seats/retainer and M04 airpath remain steel in both hybrid scenarios',
                           'Dissimilar-metal joints, coating/bonding and stiffness need review',
                           'No gauges reduced; no filter/fan/base/hardware mass assigned',
                           'Wider opening/panel/larger shell examples are NOT edited CAD or OEM tolerances',
                           'Corner calculation assumes a centred flat rectangular panel at the stated forward plane',
                           'No latch, bolt, hinge, gasket compression, hands/tools or complete service envelope modeled',
                           'A positive nominal clearance is not a manufacturing approval',
                           'Lighter casing requires new whole-device stability assessment']}


class Tests(unittest.TestCase):
    def test_nominal_gap(self):
        self.assertEqual(side_gap(635,633),1)

    def test_tolerance_clash(self):
        self.assertAlmostEqual(side_gap(635,633,1,1,1,.2),-1.4)

    def test_wider_example(self):
        self.assertAlmostEqual(side_gap(645,633,1,1,1,.2),3.6)

    def test_larger_shell(self):
        self.assertAlmostEqual(corner_clearance(980,645,15,10)-corner_clearance(950,645,15,10),15)

    def test_density_only(self):
        p=[{'group':'cosmetic_casing','volume_mm3':1e9},{'group':'frame','volume_mm3':1e9}]
        result=subtotal(p,('cosmetic_casing',))
        self.assertEqual(result['partial_material_mass_kg'],10550)
        self.assertIsNone(result['complete_machine_mass_kg'])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            side_gap(0,633)
        with self.assertRaises(ValueError):
            corner_clearance(950,645,-1,10)


if __name__=='__main__':
    output=screen()
    (ROOT/'results/fan_selection/weight_service_screen.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))
