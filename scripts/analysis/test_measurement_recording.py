"""Synthetic fixtures only; not physical AQI-TOWER results."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('recorder', Path(__file__).parents[1] / 'monitoring/record_measurements.py')
RECORDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RECORDER)


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.meta = {'run_id': 'UNIT_TEST_ONLY', 'evidence_kind': 'synthetic_test',
                     'instruments': {'TEST_PM': {'channel': 'pm25_room_a',
                                               'position_or_method': 'unit test fixture'}}}
        self.record = {'timestamp': '2026-10-03T12:00:00+05:30', 'stage': 'baseline_off',
                       'channel': 'pm25_room_a', 'value': 12, 'unit': 'ug/m3',
                       'instrument_id': 'TEST_PM', 'notes': 'synthetic test only'}

    def test_utc_and_evidence_label(self):
        row = RECORDER.validate_record(self.record, self.meta)
        self.assertEqual(row['timestamp_utc'], '2026-10-03T06:30:00+00:00')
        self.assertEqual(row['evidence_kind'], 'synthetic_test')
        self.assertEqual(row['calibration_reference'], 'UNKNOWN')

    def test_timestamp_offset_required(self):
        self.record['timestamp'] = '2026-10-03T12:00:00'
        with self.assertRaises(ValueError):
            RECORDER.validate_record(self.record, self.meta)

    def test_bad_readings_rejected(self):
        for value in (None, float('nan'), float('inf'), -1, True):
            with self.subTest(value=value):
                self.record['value'] = value
                with self.assertRaises(ValueError):
                    RECORDER.validate_record(self.record, self.meta)

    def test_unit_and_identity(self):
        self.record['unit'] = 'mg/m3'
        with self.assertRaises(ValueError):
            RECORDER.validate_record(self.record, self.meta)
        self.record['unit'] = 'ug/m3'
        self.record['instrument_id'] = 'UNREGISTERED'
        with self.assertRaises(ValueError):
            RECORDER.validate_record(self.record, self.meta)

    def test_physical_model_required(self):
        self.meta['evidence_kind'] = 'physical_measurement'
        with self.assertRaises(ValueError):
            RECORDER.validate_metadata(self.meta)

    def test_signed_pressure_allowed(self):
        self.meta['instruments']['TEST_PM']['channel'] = 'dp_hepa'
        self.record.update(channel='dp_hepa', unit='Pa', value=-2)
        self.assertEqual(RECORDER.validate_record(self.record, self.meta)['value'], -2)

    def run_import(self, folder, records):
        folder = Path(folder)
        (folder / 'meta.json').write_text(json.dumps(self.meta), encoding='utf-8')
        (folder / 'input.jsonl').write_text('\n'.join(json.dumps(r) for r in records), encoding='utf-8')
        return RECORDER.import_readings(folder / 'meta.json', folder / 'input.jsonl', folder / 'output.csv')

    def test_duplicate_or_empty_no_output(self):
        for records in ([], [self.record, self.record]):
            with tempfile.TemporaryDirectory() as folder:
                with self.assertRaises(ValueError):
                    self.run_import(folder, records)
                self.assertFalse((Path(folder) / 'output.csv').exists())

    def test_csv_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(self.run_import(folder, [self.record]), 1)
            with (Path(folder) / 'output.csv').open(newline='', encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]['evidence_kind'], 'synthetic_test')
            with self.assertRaises(FileExistsError):
                self.run_import(folder, [self.record])


if __name__ == '__main__':
    unittest.main()
