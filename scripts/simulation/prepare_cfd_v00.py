"""Read native V00 CAD, verify box solids, and generate exact conformal blockMesh.

Run with FreeCAD's bundled Python on Windows. No CAD files are modified.
Existing solution directories are protected: choose a new --case for a new run.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]
REGIONS = ['AIR_INLET', 'DIRTY_PLENUM', 'STAGE_01', 'INTERSTAGE_01',
           'STAGE_02', 'INTERSTAGE_02', 'STAGE_03', 'CLEAN_PLENUM',
           'CLEAN_RISER', 'AIR_OUTLET']


def header(name, cls='dictionary'):
    return f'FoamFile {{ version 2.0; format ascii; class {cls}; object {name}; }}\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, default=ROOT / 'cfd/V00')
    parser.add_argument('--cell-mm', type=float, default=20.0)
    args = parser.parse_args()
    case = args.case.resolve()
    if args.cell_mm <= 0:
        raise ValueError('Cell size must be positive')
    if case.exists() and any(p.is_dir() and p.name.replace('.', '', 1).isdigit()
                             and float(p.name) > 0 for p in case.iterdir()):
        raise RuntimeError('Existing results protected; select a fresh --case directory')
    source = ROOT / 'cad/parametric/AQI_Tower_ConceptA_V00.FCStd'
    doc = App.openDocument(str(source))
    doc.recompute()
    boxes, shapes = {}, []
    for name in REGIONS:
        found = [o for o in doc.Objects if getattr(o, 'CFDRegion', '') == name]
        assert len(found) == 1, (name, len(found))
        obj = found[0]
        shape = obj.Shape
        assert shape.isValid() and len(shape.Solids) == 1
        b = shape.BoundBox
        bounds = [b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax]
        rect = Part.makeBox(b.XLength, b.YLength, b.ZLength,
                            App.Vector(b.XMin, b.YMin, b.ZMin))
        assert abs(shape.Volume - rect.Volume) < 1e-3
        assert shape.cut(rect).Volume + rect.cut(shape).Volume < 1e-3, name
        boxes[name] = {'object': obj.Name, 'bounds_mm': bounds, 'volume_m3': shape.Volume * 1e-9}
        shapes.append(shape)
    for a, b in itertools.combinations(shapes, 2):
        assert a.common(b).Volume < 1e-3, 'Overlapping fluid regions'
    united = shapes[0].multiFuse(shapes[1:]).removeSplitter()
    assert united.isValid() and len(united.Solids) == 1, 'Domain must be one connected solid'
    assert abs(united.Volume - sum(s.Volume for s in shapes)) < 1e-3
    axes = [sorted({round(v['bounds_mm'][j], 8) for v in boxes.values()
                    for j in [2*d, 2*d+1]}) for d in range(3)]
    occupied = {}
    for idx in itertools.product(*(range(len(ax)-1) for ax in axes)):
        center = [(axes[d][idx[d]] + axes[d][idx[d]+1])/2 for d in range(3)]
        matches = [name for name, item in boxes.items()
                   if all(item['bounds_mm'][2*d] < center[d] < item['bounds_mm'][2*d+1] for d in range(3))]
        assert len(matches) <= 1
        if matches:
            occupied[idx] = matches[0]
    # Global vertex IDs ensure all adjoining blocks share conformal faces.
    vertices, vertex_ids = [], {}
    def vertex(idx):
        if idx not in vertex_ids:
            vertex_ids[idx] = len(vertices)
            vertices.append(tuple(axes[d][idx[d]] for d in range(3)))
        return vertex_ids[idx]
    corners = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
    faces = [((-1,0,0),(0,4,7,3)),((1,0,0),(1,2,6,5)),
             ((0,-1,0),(0,1,5,4)),((0,1,0),(3,7,6,2)),
             ((0,0,-1),(0,3,2,1)),((0,0,1),(4,5,6,7))]
    boundaries = {name: [] for name in ['AIR_INLET', 'AIR_OUTLET', 'WALLS']}
    boundary_area = {name: 0.0 for name in boundaries}
    blocks, cell_counts = [], dict.fromkeys(REGIONS, 0)
    for idx, region in occupied.items():
        ids = [vertex(tuple(idx[d]+c[d] for d in range(3))) for c in corners]
        lengths = [axes[d][idx[d]+1]-axes[d][idx[d]] for d in range(3)]
        counts = [max(1, math.ceil(v/args.cell_mm - 1e-10)) for v in lengths]
        cell_counts[region] += math.prod(counts)
        blocks.append(f"hex ({' '.join(map(str, ids))}) {region} ({' '.join(map(str, counts))}) simpleGrading (1 1 1)")
        for delta, face in faces:
            neighbor = tuple(idx[d]+delta[d] for d in range(3))
            if neighbor in occupied:
                continue
            patch = 'WALLS'
            if region == 'AIR_INLET' and delta == (-1,0,0):
                patch = 'AIR_INLET'
            elif region == 'AIR_OUTLET' and delta == (1,0,0):
                patch = 'AIR_OUTLET'
            boundaries[patch].append('('+' '.join(str(ids[i]) for i in face)+')')
            normal = next(d for d in range(3) if delta[d])
            boundary_area[patch] += math.prod(lengths[d] for d in range(3) if d != normal)*1e-6
    for sub in ['system', 'constant', '0', 'logs']:
        (case/sub).mkdir(parents=True, exist_ok=True)
    mesh = header('blockMeshDict') + '\nconvertToMeters 0.001;\nvertices\n(\n'
    mesh += '\n'.join('('+ ' '.join(f'{v:.9g}' for v in p)+')' for p in vertices)
    mesh += '\n);\nblocks\n(\n'+'\n'.join(blocks)+'\n);\nedges ();\nboundary\n(\n'
    for name, face_list in boundaries.items():
        mesh += name+'\n{\n type '+('wall' if name == 'WALLS' else 'patch')+';\n faces\n(\n'+'\n'.join(face_list)+'\n);\n}\n'
    mesh += ');\nmergePatchPairs ();\n'
    (case/'system/blockMeshDict').write_text(mesh, encoding='utf-8')
    metadata = {'source': str(source.relative_to(ROOT)), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'freecad_version': App.Version(), 'units': 'CAD mm; mesh metres', 'regions': boxes,
                'fused_solid_count': len(united.Solids), 'fluid_volume_m3': united.Volume*1e-9,
                'boundary_area_m2': boundary_area, 'block_count': len(blocks),
                'max_cell_edge_mm': args.cell_mm, 'cell_counts': cell_counts, 'total_cells': sum(cell_counts.values()),
                'excluded_object': 'TowerEnvelope', 'stage_treatment': 'EMPTY FLUID; no resistance'}
    (case/'geometry_audit.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (case/'V00.foam').touch()
    App.closeDocument(doc.Name)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
