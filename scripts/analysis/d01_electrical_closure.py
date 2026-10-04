"""E01 supplement: verified rating limits, conditional loads and open coordination.

No chosen fuse/wire/contact rating follows from this screening arithmetic.
OEM source values checked 2026-10-05; scripts never fetch or change hardware.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/prototype_d01/electrical_package'
SOURCES = {
    'fan': 'https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf',
    'supply': 'https://www.noctua.at/en/products/nv-ps1/specifications',
    'controller': 'https://www.noctua.at/en/products/na-fc1/specifications',
    'hub': 'https://www.noctua.at/en/products/na-fh1/specifications',
    'hub_functions': 'https://www.noctua.at/en/products/na-fh1/features',
    'chain': 'https://www.noctua.at/en/products/nv-ps1',
    'isolation_principle': 'https://www.hse.gov.uk/work-equipment-machinery/maintenance.htm',
}


def demand(fan_multiplier, auxiliary_A, supply_A=2.0, hub_input_A=2.0):
    args = [fan_multiplier, auxiliary_A, supply_A, hub_input_A]
    if not all(math.isfinite(x) for x in args) or fan_multiplier <= 0 or auxiliary_A < 0 or min(supply_A, hub_input_A) <= 0:
        raise ValueError('Finite positive ratings/multiplier and nonnegative auxiliary load required')
    fans = 4 * .35 * fan_multiplier
    total = fans + auxiliary_A
    limit = min(supply_A, hub_input_A, 3.0)  # NA-FC1 maximum current
    return dict(assumed_fan_current_multiplier=fan_multiplier, assumed_auxiliary_A=auxiliary_A,
                total_A=total, total_W=12*total, governing_current_limit_A=limit,
                arithmetic_margin_A=limit-total,
                exceeds_catalogue_continuous_limit=total > limit+1e-12,
                maximum_multiplier_at_assumed_auxiliary=(limit-auxiliary_A)/1.4,
                interpretation='Conditional catalogue-load screen, NOT measured inrush/trip timing or safety pass')


def copper_loop_drop(current_A, one_way_m, section_mm2, temperature_C=20):
    values = [current_A, one_way_m, section_mm2, temperature_C]
    if not all(math.isfinite(x) for x in values) or current_A < 0 or one_way_m < 0 or section_mm2 <= 0 or not -20 <= temperature_C <= 80:
        raise ValueError('Invalid current/length/section or temperature outside screening range')
    # Explicit engineering assumptions; real OEM conductors/connectors uncharacterized.
    resistance = 2*one_way_m*.0175*(1+.00393*(temperature_C-20))/section_mm2
    return dict(current_A=current_A, assumed_one_way_m=one_way_m,
                assumed_copper_section_mm2=section_mm2, assumed_temperature_C=temperature_C,
                loop_resistance_ohm=resistance, drop_V=current_A*resistance,
                conductor_loss_W=current_A**2*resistance)


def build():
    loads = [demand(k, a) for a in (0, .05, .1, .2, .5) for k in (1, 1.25, 1.5, 2)]
    drops = [copper_loop_drop(i, length, section, temp)
             for i in (.35, 1.4) for length in (.3, .7, 1.0)
             for section in (.14, .25, .5) for temp in (20, 40)]
    coverage = [
        dict(event='Mains interruption/restoration', documented_action='NV-PS1 power removal/restoration; no deliberate-start latch demonstrated', closure='UNPROVEN', required='Remove run permission; reject held START; fresh action required'),
        dict(event='Hub overload/short recovery', documented_action='OEM auto-resetting input fuses', closure='NOT A MANUAL-RESTART LATCH', required='Address recovery without defeating OEM fuses; sensing/latched response unselected'),
        dict(event='Fan2/3/4 stalls', documented_action='Per-port RPM LEDs; only fan1 RPM forwarded upstream', closure='NO INDEPENDENT FOUR-FAN PROTECTIVE FEEDBACK', required='Allocate fault response from actual hazards; independent coverage if required'),
        dict(event='PWM cable open or speed dial at minimum', documented_action='No verified whole-chain stopped-state guarantee', closure='UNKNOWN', required='Never treat PWM setting as isolation; document actual loss-of-signal response'),
        dict(event='Filter or guard servicing', documented_action='No selected reconnection-prevention assembly', closure='OPEN', required='Isolate every energy path; prevent reconnection; verify run-down before access'),
        dict(event='Logger/USB loss', documented_action='Logger separate from fan power reference', closure='ARCHITECTURE INTENT ONLY', required='No backfeed or safety dependence; physical segregation/verification still required'),
    ]
    return dict(status='E01 DIGITAL ENGINEERING COMPLETE / POWER, WIRING AND SAFETY RELEASE OPEN',
                accessed='2026-10-05', sources=SOURCES,
                verified_catalogue=dict(fan_sku='ACFAN00287A', fan_count=4, fan_typical_voltage_V=12,
                                        fan_published_current_A=.35, fan_published_start_voltage_V=3.9,
                                        supply_output_V=12, supply_max_A=2, supply_max_W=24,
                                        controller_max_A=3, controller_max_W=36,
                                        hub_selected_4pin_max_W=24, hub_unselected_SATA_max_W=54,
                                        fan_ambient_C=[0,40], supply_ambient_C=[0,40], hub_ambient_C=[-40,60],
                                        controller_environment='UNKNOWN',
                                        fan_pin_functions={'1':'Ground (-)','2':'Power (+)','3':'Tachometer output','4':'PWM control'}),
                unresolved=dict(fan_startup_A=None, startup_duration_ms=None, auxiliary_current_A=None,
                                supply_current_limit_time_curve=None, hub_fuse_time_current_curve=None,
                                OEM_conductor_cross_sections=None, connector_contact_ratings=None,
                                DC_switching_part=None, fuse_part_and_rating=None,
                                complete_restart_hardware=None, enclosure_part=None,
                                approved_minimum_running_fan_voltage_V=None),
                nominal_fan_only=demand(1,0), load_scenarios=loads,
                stronger_supply_same_hub_counterexample=demand(2,0,supply_A=5),
                voltage_drop_assumptions='Copper rho20=0.0175 ohm mm2/m; alpha=0.00393/K. Example sections/lengths/temperatures, NOT existing OEM gauge, ampacity or allowable drop. Contact, controller and supply drops excluded; 3.9V startup is NOT approved running minimum.',
                voltage_drop_scenarios=drops, fault_coverage=coverage,
                release=dict(energization=False, procurement=False, fuse_selected=False, wire_selected=False,
                             safety_function_implemented=False, physical_prototypes=0, physical_tests=0),
                recommendation='Retain external unmodified OEM adapter reference and single fan-power domain for indoor prototype. Do not insert an unselected relay, bridge the protective gap, uprate the supply alone, use SATA or parallel adapters. Finish hazard allocation and rated switching/protection/enclosure as one assembly. Existing restart requirements unchanged.')


def main():
    report = build()
    (OUT/'POWER_COORDINATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('20 load cases, 36 conditional copper-loop cases; construction release remains OPEN.')
    print(json.dumps(report['nominal_fan_only'],indent=2))


if __name__ == '__main__':
    main()
