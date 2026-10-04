"""D01 conditional electrical closure evidence; never selects protective hardware.

Standard-library only. OEM values come from retained E01/E02 evidence; scenarios
are explicitly assumed. No returned result authorizes construction or operation.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/prototype_d01/electrical_package/batch_closure'


def nonnegative(*values):
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('Inputs must be finite and nonnegative')


def power_screen(multiplier=1.0, auxiliary_A=0.0, opta_W=2.0, voltage_V=12.0):
    nonnegative(multiplier, auxiliary_A, opta_W, voltage_V)
    if voltage_V == 0:
        raise ValueError('Supply voltage must be positive')
    fans = 4 * .35 * multiplier
    controls = opta_W / voltage_V
    total = fans + controls + auxiliary_A
    return dict(fan_multiplier_ASSUMED=multiplier, auxiliary_A_ASSUMED=auxiliary_A,
                fan_path_A=fans, source_total_A=total,
                source_margin_A=2-total, fan_path_margin_A=2-fans,
                candidate_fuse_typical40C_margin_A=1.7-total,
                source_multiplier_ceiling=(2-controls-auxiliary_A)/1.4,
                within_source_continuous_screen=total <= 2,
                within_fan_path_continuous_screen=fans <= 2,
                startup_approved=False)


def copper_screen(length_one_way_m, area_mm2, current_A, temperature_C=20,
                  source_V=12, contacts_total_ohm=0):
    nonnegative(length_one_way_m, area_mm2, current_A, source_V, contacts_total_ohm)
    if not math.isfinite(temperature_C) or temperature_C < -50 or area_mm2 == 0:
        raise ValueError('Invalid conductor temperature/area')
    # ASSUMED copper resistivity and coefficient, not certified cable resistance.
    resistance = 2*length_one_way_m*.0175/area_mm2*(1+.00393*(temperature_C-20))
    resistance += contacts_total_ohm
    drop = current_A*resistance
    return dict(one_way_m_ASSUMED=length_one_way_m, area_mm2_ASSUMED=area_mm2,
                temperature_C_ASSUMED=temperature_C, current_A_ASSUMED=current_A,
                connector_resistance_ohm_ASSUMED=contacts_total_ohm,
                loop_ohm=resistance, drop_V=drop, receiving_V=source_V-drop,
                conductor_loss_W=current_A**2*resistance,
                wire_ampacity_approved=False)


def input_screen(source_V=12, series_ohm=0, impedance_ohm=8900):
    nonnegative(source_V, series_ohm, impedance_ohm)
    if impedance_ohm == 0:
        raise ValueError('Impedance must be positive')
    current = source_V/(impedance_ohm+series_ohm)
    voltage = current*impedance_ohm
    return dict(source_V_ASSUMED=source_V, series_ohm_ASSUMED=series_ohm,
                nominal_input_mA=current*1000, input_V=voltage,
                high_threshold_margin_V=voltage-6.6,
                nominal_HIGH_screen=voltage >= 6.6,
                minimum_contact_load_approved=False)


def build():
    evidence = [ROOT/'reports/prototype_d01/electrical_package'/f for f in
                ('POWER_COORDINATION.json', 'OPTA_INTEGRATION_SCREEN.json', 'OPTA_BOARD_BUILD.json')]
    sources = dict(
        opta='https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf',
        contact_faq='https://www.se.com/us/en/faqs/FA100572/',
        current_contact_catalogue='https://www.se.com/us/en/download/document/0100CT2401-SEC-19/',
        hub='https://www.noctua.at/en/products/na-fh1/specifications',
        hub_reset='https://www.noctua.at/en/products/na-fh1/features',
        supply='https://www.noctua.at/en/products/nv-ps1/specifications',
        fuse='https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1')
    nominal = power_screen()
    data = dict(status='CONDITIONAL DIGITAL SCREEN / NOT FOR WIRING OR ENERGIZATION',
                access_date='2026-10-05', sources=sources,
                inherited_evidence_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence},
                nominal=nominal,
                power_scenarios=[power_screen(m,a) for m in (1,1.2,1.3,1.4,1.5,2) for a in (0,.05,.1,.2)],
                cable_scenarios=[copper_screen(l,a,i,t,12,.05) for l in (.5,1,2) for a in (.5,.75,1) for i in (.35,1.5666666666666667) for t in (20,60)],
                nominal_input_screen=input_screen(),
                input_series_scenarios=[input_screen(v,r) for v in (10.2,12) for r in (0,10,100,1000)],
                opta_supply_limits=dict(recommended_min_V=12,permissible_min_V=10.2,
                                       at_nominal_source_recommended_drop_margin_V=0,
                                       at_nominal_source_permissible_drop_margin_V=1.8,
                                       actual_supply_tolerance_and_transients_V=None),
                fuse_counterexample=dict(candidate='0297002.WXNV / NOT SELECTED',
                    conditional_source_fault_limit_A=2,
                    fault_to_fuse_rating_ratio=1,
                    fuse110percent_current_A=2.2,
                    fuse135percent_current_A=2.7,
                    fuse200percent_current_A=4,
                    fuse110percent_min_opening_s=360000,
                    note='ASSUMED sustained2A limiting does not reach any of these overcurrent test points. No guaranteed clearing follows. Actual PSU/hub current-time and recovery remain unknown.',
                    fault_clearing_approved=False),
                actual_unknowns=['PSU voltage tolerance/ripple/transient and fault-current/recovery profile',
                    'All4 simultaneous fan starting current/time; hub and NA-FC1 operating current',
                    'Switching/isolating device ratings and protective architecture',
                    'OEM wire/contact sizes, installed lengths, ampacity/temperature, routing and connectors',
                    'ZBE1016/1026 present-part minimum switching load and assembled contact terminal IDs',
                    'Fan/hub downstream reset detection and independent manual restart implementation',
                    'Approved ambient/closed-enclosure temperature and site upstream protection'])
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'ELECTRICAL_BATCH_SCREEN.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    rows = [
        ('W01','NV-PS1 OEM output','proposed DC distribution','OEM NA-AC10 / distribution adapter unresolved','12V / source max2A','UNKNOWN','Source protection, polarity, strain relief, source tolerance'),
        ('W02','DC distribution','NA-FC1 input then NA-FH1 four-pin input','OEM connectors; exact installed distribution unselected','fan path nominal1.4A; ceiling2A','UNKNOWN','No splicing release; OEM conductor/contact data and fault curve'),
        ('W03-06','NA-FH1 output ports1-4','P14 Max fans1-4','OEM pin1GND/2power/3tach/4PWM','each published0.35A; startup UNKNOWN','UNKNOWN','Final connector envelope/extension/entry/retention; no cut OEM lead'),
        ('W07','proposed protected unswitched DC branch','Opta supply + and -','OEM labelled supply terminals; distribution unselected','max2W at12V =0.167A screen','UNKNOWN','Supply2W budget; branch fuse, conductor and distribution terminals'),
        ('W08','proposed protected DC sense branch via START NO','Opta I1 / A0','ZBE1016 contact screw IDs UNVERIFIED','nominal1.348mA resistance screen','UNKNOWN','0.5mm2 minimum Opta accepted wire, not cable selection'),
        ('W09','proposed protected DC sense branch via STOP NC','Opta I2 / A1','ZBE1026 contact screw IDs UNVERIFIED','nominal1.348mA; HIGH healthy','UNKNOWN','Broken wire inhibits ordinary request, not safety fault tolerance'),
        ('W10','proposed protected DC sense branch via RESET NO','Opta I3 / A2','ZBE1016 contact screw IDs UNVERIFIED','nominal1.348mA resistance screen','UNKNOWN','RESET not fan START; low-load compatibility open'),
        ('W11','reviewed bench permissive','Opta I4 / A3','NO protective field interface selected','ordinary bench input','UNKNOWN','Must not substitute for PR1 protective path'),
        ('W12','proposed protected unswitched DC sense','Opta I5 / A4','digital mode only','nominal1.348mA resistance screen','UNKNOWN','Not fan branch voltage or downstream reset proof'),
        ('W13','Opta relay outputs1-4','NO FAN CONNECTION','default D0-D3 LOW','all outputs disabled','not connected','Do not energize fans with bench review sketch'),
        ('W14','Opta functional earth / metal panel','reviewed reference/bonding point','OEM FE is not a substitute for PE','UNKNOWN','UNKNOWN','Qualified classification and OEM FE/bonding; no invented mains PE route'),
        ('W15','USB/service instruments','controller/logger','additional source/backfeed domain','UNKNOWN','UNKNOWN','Identify/disconnect or review all service energy sources')]
    with (OUT/'CABLE_AND_INTERFACE_SCHEDULE.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f); writer.writerow(('ID','From_function','To_function','Verified_interface_or_unknown','Load_basis','Installed_length','Exact_release_dependency'));writer.writerows(rows)
    return data


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.parse_args()
    result=build()
    print(json.dumps({'output':str(OUT),'power_cases':len(result['power_scenarios']),
                      'cable_cases':len(result['cable_scenarios']),'status':result['status']}))
