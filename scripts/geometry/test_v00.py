"""Checks geometry closure, orientation and bad-input rejection without a CFD claim."""
import copy
import json
import unittest
from collections import Counter
from build_v00 import CONFIG, geometry


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads(CONFIG.read_text())

    def test_closed_outward_boundary_and_volume(self):
        vertices, patches, _ = geometry(self.c)
        edges = Counter()
        volume = 0
        for faces in patches.values():
            for face in faces:
                for a, b in zip(face, face[1:] + face[:1]):
                    edges[a, b] += 1
                a,b,c = [vertices[i] for i in face[:3]]
                ab,ac = [b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)]
                n = (ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
                centre = [sum(v[i] for v in vertices)/8 for i in range(3)]
                self.assertGreater(sum(n[i]*(a[i]-centre[i]) for i in range(3)), 0)
                volume += sum(a[i]*n[i] for i in range(3))/3
        self.assertTrue(all(edges[b,a] == count == 1 for (a,b),count in edges.items()))
        expected = self.c['tower_width']['value']*self.c['tower_depth']['value']*self.c['tower_height']['value']
        self.assertAlmostEqual(volume, expected)

    def test_reject_invalid_dimensions_and_mesh(self):
        for value in [0,-1,float('nan'),float('inf'),True]:
            c = copy.deepcopy(self.c)
            c['tower_height']['value'] = value
            with self.assertRaises(ValueError): geometry(c)
        self.c['mesh_cells']['value'] = [1,0,2]
        with self.assertRaises(ValueError): geometry(self.c)


if __name__ == '__main__': unittest.main()
