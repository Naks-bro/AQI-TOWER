"""Preliminary sizing only; not CFD, certified CADR, or a fabrication release.

Run: python scripts/analysis/build_screening.py
Inputs are deliberately explicit. Historical curves remain unverified for procurement.
"""
import json
import math
from pathlib import Path
import unittest

CURVE = [(0, 688), (375, 640), (750, 480), (914, 388), (1200, 205), (1501, 0)]


def fan_pressure(q):
    if not 0 <= q <= CURVE[-1][0]:
        raise ValueError("Flow outside historical fan curve; do not extrapolate")
    for (qa, pa), (qb, pb) in zip(CURVE, CURVE[1:]):
        if qa <= q <= qb:
            return pa + (pb - pa) * (q - qa) / (qb - qa)
    raise ValueError("Invalid curve")


def losses(q, prefilter=25, hepa_factor=1, duct_at_1332=3.8, extra_at_1300=0):
    # Filter linear extrapolation is an assumption, not a measured curve.
    return ((111.2 * hepa_factor + prefilter) * q / 1332
            + duct_at_1332 * (q / 1332) ** 2
            + extra_at_1300 * (q / 1300) ** 2)


def operating_point(**kwargs):
    lo, hi = 0.0, float(CURVE[-1][0])
    for _ in range(80):
        mid = (lo + hi) / 2
        if fan_pressure(mid) > losses(mid, **kwargs):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def report():
    scenarios = {
        "historical_sealed_HEPA_only": {"prefilter": 0},
        "clean_prefilter_25Pa_optimistic_duct": {},
        "clean_prefilter_45Pa_optimistic_duct": {"prefilter": 45},
        "prefilter_80Pa_optimistic_duct": {"prefilter": 80},
        "clean_prefilter_added_50Pa_at_1300": {"extra_at_1300": 50},
        "HEPA_twice_clean_resistance_added_50Pa": {"hepa_factor": 2, "extra_at_1300": 50},
    }
    q = 1300
    velocity = q / 3600 / (math.pi * 0.25 ** 2 / 4)
    return {
        "status": "PRELIMINARY SCREENING; all scenarios unvalidated; no carbon loss included",
        "inputs": {"fan_curve": CURVE, "HEPA_Pa_at_1332": 111.2,
                   "historical_residual_duct_Pa_at_1332": 3.8,
                   "air_density_kg_m3_assumption": 1.2},
        "scenarios_m3_h": {k: round(operating_point(**v), 1) for k, v in scenarios.items()},
        "illustrative_1300_m3_h": {
            "HEPA_gross_face_velocity_m_s": round(q / 3600 / (0.593 ** 2), 3),
            "250mm_duct_velocity_m_s": round(velocity, 3),
            "250mm_duct_dynamic_pressure_Pa": round(0.5 * 1.2 * velocity ** 2, 2),
            "remaining_pressure_at_1300_Pa_clean25_no_carbon": round(fan_pressure(q) - losses(q), 2),
            "remaining_pressure_at_1200_Pa_clean25_no_carbon": round(fan_pressure(1200) - losses(1200), 2),
            "carbon_volume_L_for_assumed_0_1s_EBCT": round(q / 3600 * 0.1 * 1000, 2),
            "carbon_depth_mm_at_gross_HEPA_area_for_0_1s_EBCT": round(q / 3600 * 0.1 / 0.593 ** 2 * 1000, 2),
            "illustrative_CADR_at_assumed_90pct_whole_device_efficiency_m3_h": q * 0.9,
            "enclosed_area_m2_at_assumed_5ACH_3m_height_90pct_efficiency": q * 0.9 / (5 * 3),
            "outdoor_advective_flow_m3_h_at_1m_s_10m_width_2m_height": 1 * 10 * 2 * 3600,
            "tower_to_example_outdoor_advective_flow_ratio": round(q / 72000, 5),
            "fan_only_energy_kWh_8h_at_historical_301W": 301 * 8 / 1000,
        },
        "limitations": ["No outdoor radius or pollutant reduction inferred from flow ratio",
                        "Room sizing assumes mixing; not a certification or school ventilation recommendation",
                        "Carbon EBCT alone does not establish adsorption performance",
                        "Fan SKU, curves, full duct losses and filter loading require verification"],
    }


class Checks(unittest.TestCase):
    def test_curve(self):
        for q, p in CURVE:
            self.assertAlmostEqual(fan_pressure(q), p)
        with self.assertRaises(ValueError):
            fan_pressure(1600)

    def test_balance(self):
        q = operating_point(extra_at_1300=50)
        self.assertAlmostEqual(fan_pressure(q), losses(q, extra_at_1300=50), places=8)

    def test_loading_reduces_flow(self):
        self.assertGreater(operating_point(), operating_point(prefilter=80))
        self.assertGreater(operating_point(), operating_point(extra_at_1300=50))
        self.assertGreater(operating_point(), operating_point(hepa_factor=2))

    def test_zero_flow_zero_system_loss(self):
        self.assertEqual(losses(0), 0)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
    if not unittest.TextTestRunner().run(suite).wasSuccessful():
        raise SystemExit(1)
    output = Path(__file__).resolve().parents[2] / "results" / "build_screening.json"
    output.write_text(json.dumps(report(), indent=2) + "\n", encoding="utf-8")
    print(output)
    print(json.dumps(report(), indent=2))
