"""Generate the V00 domain and OpenFOAM mesh dictionary. Standard library only."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'cad/parametric/v00.json'


def geometry(config):
    dims = [config[k]['value'] for k in ('tower_width', 'tower_depth', 'tower_height')]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0 for v in dims):
        raise ValueError('Dimensions must be finite positive metres')
    cells = config['mesh_cells']['value']
    if len(cells) != 3 or any(type(n) is not int or n < 1 for n in cells):
        raise ValueError('mesh_cells must contain three positive integers')
    w, d, h = dims
    vertices = [(0,0,0),(w,0,0),(w,d,0),(0,d,0),(0,0,h),(w,0,h),(w,d,h),(0,d,h)]
    faces = {'inlet': [(0,3,2,1)], 'outlet': [(4,5,6,7)],
             'walls': [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]}
    return vertices, faces, cells


def header(kind, name):
    return f'FoamFile\n{{\n    version 2.0;\n    format ascii;\n    class {kind};\n    object {name};\n}}\n'


def build():
    config = json.loads(CONFIG.read_text())
    vertices, faces, cells = geometry(config)
    exports = ROOT / 'cad/exports'
    system = ROOT / 'cfd/V00_empty_tower/system'
    exports.mkdir(parents=True, exist_ok=True)
    system.mkdir(parents=True, exist_ok=True)
    obj = '# CONCEPTUAL air domain; coordinates in metres; not enclosure material\n'
    obj += ''.join('v ' + ' '.join(map(str, v)) + '\n' for v in vertices)
    for name, polygons in faces.items():
        obj += f'g {name}\n'
        obj += ''.join('f ' + ' '.join(str(i+1) for i in f) + '\n' for f in polygons)
    (exports / 'v00_air_domain.obj').write_text(obj)
    body = header('dictionary', 'blockMeshDict') + 'convertToMeters 1;\nvertices\n(\n'
    body += ''.join('    (' + ' '.join(map(str, v)) + ')\n' for v in vertices)
    body += ');\nblocks\n(\n    hex (0 1 2 3 4 5 6 7) (' + ' '.join(map(str, cells)) + ') simpleGrading (1 1 1)\n);\nedges ();\nboundary\n(\n'
    for name, polygons in faces.items():
        body += f'    {name}\n    {{\n        type {"wall" if name == "walls" else "patch"};\n        faces\n        (\n'
        body += ''.join('            (' + ' '.join(map(str, f)) + ')\n' for f in polygons)
        body += '        );\n    }\n'
    body += ');\nmergePatchPairs ();\n'
    (system / 'blockMeshDict').write_text(body)
    (system / 'controlDict').write_text(header('dictionary', 'controlDict') +
        'application blockMesh;\nstartFrom startTime;\nstartTime 0;\nstopAt endTime;\nendTime 0;\ndeltaT 1;\nwriteControl timeStep;\nwriteInterval 1;\nwriteFormat ascii;\nwritePrecision 10;\nrunTimeModifiable false;\n')
    print('Generated CONCEPTUAL geometry and mesh-only V00 case. No CFD solution.')


if __name__ == '__main__':
    build()
