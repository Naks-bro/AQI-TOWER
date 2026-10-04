"""Regression checks on the executed FreeCAD study, not structural certification."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SegmentedAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT/'cad/packaging/M02_SEGMENTED_FRAME_AUDIT.json').read_text(encoding='utf-8'))

    def test_expected_shapes(self):
        self.assertEqual(self.audit['valid_route_solids'], 28)
        self.assertEqual(self.audit['integrated_snapshot_solids'], 41)

    def test_nominal_clashes(self):
        self.assertEqual(self.audit['nominal_positive_volume_conflicts'], [])
        self.assertEqual(self.audit['route_internal_positive_volume_conflicts'], [])

    def test_service_sweep(self):
        self.assertEqual(self.audit['assumed_HEPA_sweep_conflicts'], [])

    def test_contacts(self):
        contacts = self.audit['nominal_post_cap_plate_contacts']
        self.assertEqual(len(contacts), 16)
        self.assertEqual({c['z_mm'] for c in contacts}, {445,450,640,645})
        self.assertTrue(all(c['nominal_face_contact_mm2'] == 1225 for c in contacts))

    def test_roundtrips(self):
        for name in ('STEP_reimport','native_reopen','integrated_native_reopen_and_STEP_reimport'):
            self.assertEqual(self.audit[name], 'PASS')

    def test_source_preserved(self):
        for relative, expected in self.audit['source_sha256_unchanged'].items():
            self.assertEqual(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
