"""Fan comparison with explicit assumed clean/loaded loss envelopes; not new CFD."""
import csv
import json
from pathlib import Path
import unittest
from build_screening import CURVE

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = json.loads((ROOT / "data/fans/sp_td2000_315_silent_ecowatt_screening.json").read_text(encoding="utf-8"))
FANS = {"historical_KVO250_variant_unresolved": CURVE,
        "SP_TD2000_315_SILENT_digitized_10V": CANDIDATE["curve_points_m3h_Pa"]}
# New hardware allowance replaces, rather than adds to, historical 3.8 Pa residual.
SCENARIOS = {
    "clean_moderate_hardware": (1, 25, 50),
    "clean_restrictive_hardware": (1, 45, 100),
    "HEPA_2x_clean_prefilter": (2, 25, 50),
    "HEPA_2x_prefilter80_restrictive": (2, 80, 100),
}


def interp(curve, flow):
    if not curve[0][0] <= flow <= curve[-1][0]:
        raise ValueError("No fan-curve extrapolation allowed")
    for (qa, pa), (qb, pb) in zip(curve, curve[1:]):
        if qa <= flow <= qb:
            return pa + (pb - pa) * (flow - qa) / (qb - qa)
    raise ValueError("Invalid curve")


def pressure(flow, scenario):
    hepa_factor, prefilter_pa_at1332, hardware_pa_at1300 = SCENARIOS[scenario]
    return ((111.2 * hepa_factor + prefilter_pa_at1332) * flow / 1332
            + hardware_pa_at1300 * (flow / 1300) ** 2)


def intersection(curve, scenario, offset=0):
    lo, hi = curve[0][0], curve[-1][0]
    residual = lambda q: max(0, interp(curve, q) + offset) - pressure(q, scenario)
    if residual(lo) < 0 or residual(hi) > 0:
        raise ValueError("Operating point not bracketed by supplied curve")
    for _ in range(80):
        mid = (lo + hi) / 2
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def results():
    rows = []
    for name, curve in FANS.items():
        for scenario in SCENARIOS:
            q = intersection(curve, scenario)
            rows.append({"fan": name, "scenario": scenario, "flow_m3h": round(q, 1),
                         "operating_static_pressure_Pa": round(pressure(q, scenario), 1),
                         "pressure_required_at1300_Pa": round(pressure(1300, scenario), 1),
                         "fan_pressure_at1300_Pa": round(interp(curve, 1300), 1),
                         "margin_at1300_Pa": round(interp(curve, 1300) - pressure(1300, scenario), 1)})
    sensitivities = {s: [round(intersection(FANS["SP_TD2000_315_SILENT_digitized_10V"], s, shift), 1)
                        for shift in (-25, 25)] for s in SCENARIOS}
    return {"status": "PRELIMINARY SCREENING; all losses unmeasured; no certified duty or selection",
            "rows": rows, "SP_digitization_only_flow_range_m3h": sensitivities,
            "scenario_inputs": {s: {"HEPA_clean111_2Pa_at1332_multiplier": x[0],
                                     "prefilter_Pa_at1332": x[1], "all_hardware_Pa_at1300": x[2]}
                                for s, x in SCENARIOS.items()},
            "limitations": ["Historical HEPA extrapolation transferred only for sensitivity; new cassette not validated",
                            "Hardware allowance includes guards duct transitions and outlet; no 3.8Pa historic residual added",
                            "Loaded multiplier and prefilter80 are scenarios not OEM terminal settings",
                            "SP digitization range excludes installation filter source and density uncertainty",
                            "Static/total pressure and outlet velocity effects must be reconciled at final selection",
                            "No outdoor radius, room CADR, or power prediction derived"]}


def svg_plot():
    # Vector technical plot, generated from calculation inputs, not marketing artwork.
    x = lambda q: 85 + q / 1700 * 700
    y = lambda p: 505 - p / 800 * 400
    items = ['<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="620" viewBox="0 0 1040 620">',
             '<rect width="1040" height="620" fill="white"/>',
             '<g font-family="Arial" fill="#183446">',
             '<text x="65" y="36" font-size="23">Fan versus filter + hardware losses</text>',
             '<text x="65" y="64" font-size="14">PRELIMINARY / unmeasured loss scenarios / digitized candidate curve</text>']
    for p in range(0, 801, 100):
        items.append(f'<path d="M85 {y(p)} H785" stroke="#e2e8ec"/><text x="45" y="{y(p)+5}" font-size="13">{p}</text>')
    for q in range(0, 1701, 200):
        items.append(f'<path d="M{x(q)} 105 V505" stroke="#e2e8ec"/><text x="{x(q)-13}" y="528" font-size="13">{q}</text>')
    items.append('<text x="88" y="93" font-size="13">Pressure Pa</text><text x="350" y="562" font-size="14">Airflow m3/h</text>')
    for (name, curve), color, label in zip(FANS.items(), ['#ae5c38','#176eaa'], ['Historical KVO, identity unresolved','S&amp;P TD2000/315, chart estimate']):
        pts = ' '.join(f'{x(q)},{y(p)}' for q, p in curve)
        items.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>')
        position = 120 if color == '#ae5c38' else 178
        items.append(f'<text x="800" y="{position}" font-size="12" fill="{color}">{label.split(",")[0]}</text>')
    for scenario, color, legend_y in [('clean_moderate_hardware','#21875f',250),('HEPA_2x_prefilter80_restrictive','#aa4079',308)]:
        # Plot only points inside chart bounds, avoiding misleading clipped line joins.
        pts = ' '.join(f'{x(q)},{y(pressure(q,scenario))}' for q in range(0,1701,10) if pressure(q,scenario)<=800)
        items.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="7 4"/>')
        label = 'Clean + moderate loss' if legend_y==250 else 'Loaded + restrictive loss'
        items.append(f'<text x="800" y="{legend_y}" font-size="12" fill="{color}">{label}</text>')
        for curve in FANS.values():
            q = intersection(curve,scenario)
            items.append(f'<circle cx="{x(q)}" cy="{y(pressure(q,scenario))}" r="5" fill="{color}"/>')
    items.append('<text x="85" y="594" font-size="13">Intersections estimate delivered flow. Dirty filters lower flow. Not a purchasing approval.</text></g></svg>')
    return '\n'.join(items)


class Tests(unittest.TestCase):
    def test_exact_knots_and_bounds(self):
        for curve in FANS.values():
            for q, p in curve:
                self.assertAlmostEqual(interp(curve,q),p)
            with self.assertRaises(ValueError):
                interp(curve,curve[-1][0]+1)

    def test_balance(self):
        for curve in FANS.values():
            for s in SCENARIOS:
                q=intersection(curve,s)
                self.assertAlmostEqual(interp(curve,q),pressure(q,s),places=8)

    def test_load_reduces_flow(self):
        for curve in FANS.values():
            self.assertGreater(intersection(curve,'clean_moderate_hardware'),intersection(curve,'HEPA_2x_prefilter80_restrictive'))

    def test_chart_uncertainty_order(self):
        curve=FANS['SP_TD2000_315_SILENT_digitized_10V']
        for s in SCENARIOS:
            self.assertLess(intersection(curve,s,-25),intersection(curve,s,25))

    def test_new_hardware_replaces_historic_residual(self):
        self.assertAlmostEqual(pressure(1300,'clean_moderate_hardware'),(111.2+25)*1300/1332+50)


if __name__=='__main__':
    if not unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests)).wasSuccessful():
        raise SystemExit(1)
    out=ROOT/'results/fan_selection'
    out.mkdir(parents=True,exist_ok=True)
    result=results()
    (out/'duty_screen.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    with (out/'duty_screen.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(result['rows'][0]))
        writer.writeheader()
        writer.writerows(result['rows'])
    (out/'fan_system_screen.svg').write_text(svg_plot(),encoding='utf-8')
    print(json.dumps(result,indent=2))
