"""Regression checks of executed hatch CAD, not mechanism or leakage validation."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


class HatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=json.loads((ROOT/'cad/packaging/M05_HEPA_HATCH_AUDIT.json').read_text(encoding='utf-8'))

    def test_valid_geometry(self):
        self.assertEqual(self.audit['valid_solids'],48)
        self.assertEqual(self.audit['native_reopen_and_STEP_reimport'],'PASS')

    def test_clashes_and_filter_sweeps(self):
        self.assertEqual(self.audit['positive_volume_clashes'],[])
        self.assertTrue(all(not v for v in self.audit['assumed_filter_service_sweep_clashes'].values()))

    def test_cover_removal(self):
        self.assertEqual(self.audit['assumed_cover_forward_removal_clashes'],[])

    def test_study_dimensions(self):
        self.assertEqual(self.audit['retainer_nominal_side_margin_mm'],6)
        self.assertEqual(self.audit['casing_inner_diameter_mm_ASSUMED'],980)
        self.assertEqual(self.audit['latch_location_count_NOT_SELECTED_HARDWARE'],8)

    def test_pressure_arithmetic(self):
        self.assertAlmostEqual(self.audit['door_pressure_force_N_at_ASSUMED_500Pa'],99.975)

    def test_sources_preserved(self):
        for relative,digest in self.audit['source_sha256_unchanged'].items():
            self.assertEqual(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(),digest)


if __name__=='__main__':
    unittest.main()
