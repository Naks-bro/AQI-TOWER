"""Executed CAD regression checks, not fabrication or performance validation."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


class IndependentHousingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=json.loads((ROOT/'cad/packaging/M03_INDEPENDENT_HOUSING_AUDIT.json').read_text(encoding='utf-8'))

    def test_solids_and_roundtrip(self):
        self.assertEqual(self.audit['valid_solids'],36)
        self.assertEqual(self.audit['native_reopen_and_STEP_reimport'],'PASS')

    def test_clashes(self):
        self.assertEqual(self.audit['positive_volume_clashes'],[])

    def test_removal_sweeps(self):
        self.assertTrue(all(not v for v in self.audit['assumed_service_sweep_clashes_panels_removed'].values()))

    def test_nominal_support_contacts(self):
        contacts=self.audit['nominal_seat_to_side_rail_contacts']
        self.assertEqual(len(contacts),8)
        self.assertTrue(all(c['nominal_contact_mm2']==1225 for c in contacts))

    def test_margins_recorded_not_approved(self):
        self.assertEqual(self.audit['housing_to_post_gap_mm'],6)
        self.assertEqual(self.audit['retainer_to_inner_service_opening_side_margin_mm'],1)

    def test_source_preserved(self):
        for path,digest in self.audit['source_sha256_unchanged'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)


if __name__=='__main__':
    unittest.main()
