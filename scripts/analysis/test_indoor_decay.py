"""All readings below are generated mathematical fixtures, NOT tower measurements."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import math
import unittest
import indoor_decay as decay


class IndoorDecayTests(unittest.TestCase):
    def setUp(self):
        self.rows = []
        start = datetime(2026, 10, 3, tzinfo=timezone.utc)
        self.plan = {'run_id': 'SYNTHETIC_UNIT_TEST', 'environment': 'indoor',
                     'channel': 'pm25_room_a', 'instrument_id': 'TEST_ONLY',
                     'room_volume_m3': 100, 'volume_basis': 'assumed',
                     'usable_pm_floor_ug_m3': 0,
                     'well_mixed_assumption': True, 'matched_ventilation_declared': True,
                     'stable_sources_declared': True}
        for stage, offset, rate in [('baseline_off', 0, .5), ('tower_on', 2, 2)]:
            stamps = [(start + timedelta(hours=offset + i / 10)).isoformat() for i in range(6)]
            self.plan[stage] = {'start': stamps[0], 'end': stamps[-1]}
            for i, stamp in enumerate(stamps):
                self.rows.append({'timestamp_utc': stamp, 'stage': stage,
                                  'run_id': self.plan['run_id'], 'evidence_kind': 'synthetic_test',
                                  'channel': 'pm25_room_a', 'instrument_id': 'TEST_ONLY',
                                  'value': 100 * math.exp(-rate * i / 10), 'unit': 'ug/m3',
                                  'calibration_reference': 'UNKNOWN'})

    def test_exact_exponential(self):
        result = decay.analyze(self.rows, self.plan)
        self.assertAlmostEqual(result['conditional_clean_air_flow_m3h'], 150)
        self.assertEqual(result['evidence_kind'], 'synthetic_test')

    def test_missing_assumptions_withholds(self):
        self.plan['well_mixed_assumption'] = False
        self.assertIsNone(decay.analyze(self.rows, self.plan)['conditional_clean_air_flow_m3h'])

    def test_negative_difference_not_clipped(self):
        for row in self.rows[6:]:
            row['value'] = 100
        result = decay.analyze(self.rows, self.plan)
        self.assertLess(result['conditional_clean_air_flow_m3h'], 0)

    def test_bad_values_and_short_window(self):
        for value in (0, -1, float('nan'), float('inf')):
            rows = deepcopy(self.rows)
            rows[0]['value'] = value
            with self.assertRaises(ValueError):
                decay.analyze(rows, self.plan)
        with self.assertRaises(ValueError):
            decay.analyze(self.rows[2:], self.plan)

    def test_time_and_overlap_rejected(self):
        rows = deepcopy(self.rows)
        rows[1]['timestamp_utc'] = rows[0]['timestamp_utc']
        with self.assertRaises(ValueError):
            decay.analyze(rows, self.plan)
        with self.assertRaises(ValueError):
            decay.stamp('2026-10-03T00:00:00')
        self.plan['tower_on']['start'] = self.plan['baseline_off']['start']
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)

    def test_mixed_evidence_or_units_rejected(self):
        self.rows[0]['evidence_kind'] = 'physical_measurement'
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)
        self.rows[0]['evidence_kind'] = 'synthetic_test'
        self.rows[0]['unit'] = 'mg/m3'
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)

    def test_outdoor_and_bad_volume_rejected(self):
        self.plan['environment'] = 'outdoor'
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)
        self.plan['environment'] = 'indoor'
        self.plan['room_volume_m3'] = 0
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)

    def test_physical_floor_required(self):
        for row in self.rows:
            row['evidence_kind'] = 'physical_measurement'
        with self.assertRaises(ValueError):
            decay.analyze(self.rows, self.plan)


if __name__ == '__main__':
    unittest.main()
