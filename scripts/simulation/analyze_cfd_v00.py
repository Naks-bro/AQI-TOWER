"""Extract traceable V00 metrics and render actual fields with WSL pvpython.

Usage: pvpython --force-offscreen-rendering analyze_cfd_v00.py [case-directory]
No synthetic field or trajectory is generated. Results are numerical baseline only.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
import numpy as np
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersVerdict import vtkCellSizeFilter
from vtkmodules.vtkFiltersCore import vtkCellCenters, vtkCutter
from vtkmodules.vtkCommonDataModel import vtkPlane
from paraview import servermanager
from paraview.simple import *

ROOT = Path(__file__).resolve().parents[2]
CASE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT/'cfd/V00'
OUT = ROOT/'results/CFD_V00'
OUT.mkdir(parents=True, exist_ok=True)
RHO = 1.20


def patch_values(path, patch, components=1, count=None):
    text = path.read_text()
    match = re.search(r'\b'+re.escape(patch)+r'\s*\{([^{}]*)\}', text, re.S)
    if not match:
        raise ValueError(f'Missing patch {patch} in {path}')
    body = match[1]
    values = re.search(r'\bvalue\s+nonuniform\s+List<\w+>\s+(\d+)\s*\((.*?)\)\s*;', body, re.S)
    if values:
        arr = np.fromstring(values[2].replace('(', ' ').replace(')', ' '), sep=' ')
        assert arr.size == int(values[1])*components
        return arr.reshape(-1, components) if components > 1 else arr
    values = re.search(r'\bvalue\s+uniform\s+([^;]+);', body)
    if values:
        arr = np.fromstring(values[1].replace('(', ' ').replace(')', ' '), sep=' ')
        assert arr.size == components and count is not None
        return np.tile(arr, (count, 1)) if components > 1 else np.full(count, arr[0])
    raise ValueError(f'Missing explicit patch values in {path}: {patch}')


def leaves(dataset):
    if dataset.IsA('vtkMultiBlockDataSet'):
        for i in range(dataset.GetNumberOfBlocks()):
            b = dataset.GetBlock(i)
            if b is not None:
                yield from leaves(b)
    elif dataset.GetNumberOfCells():
        yield dataset


def sizes(dataset, array):
    alg = vtkCellSizeFilter()
    alg.SetInputData(dataset)
    alg.Update()
    return vtk_to_numpy(alg.GetOutput().GetCellData().GetArray(array))


# Combine log files: original run (0–3000) + first continuation (3001–6000 SIMPLEC).
# The second continuation (6001–9000, classic SIMPLE) was a diagnostic run that
# performed worse; results are extracted from timestep 6000 (best SIMPLEC run).
BEST_TIME = 6000.0
log_orig = (CASE/'logs/foamRun.log').read_text()
log_cont = (CASE/'logs/foamRun_continue.log').read_text()
if not re.search(r'\nEnd\s*$', log_orig):
    raise RuntimeError('Original solver log did not end cleanly')
# Combined log: original + first continuation segment up to Time = 6000
log = log_orig.rstrip() + '\n' + log_cont
times = sorted((p for p in CASE.iterdir() if p.is_dir() and re.fullmatch(r'\d+(?:\.\d+)?', p.name)
                and float(p.name) > 0), key=lambda p: float(p.name))
# Use the 6000 timestep (SIMPLEC best result) rather than the latest (9000)
final = next((t for t in times if abs(float(t.name) - BEST_TIME) < 1), times[-1])
print(f'Analysing fields from timestep: {final.name}')
rows = []
for segment in re.split(r'\nTime = ', log)[1:]:
    iteration = float(re.match(r'[\d.eE+-]+', segment)[0])
    row = {'iteration': iteration}
    for field, initial, last in re.findall(r'Solving for (\w+), Initial residual = ([\d.eE+-]+), Final residual = ([\d.eE+-]+)', segment):
        row[field+'_initial'] = float(initial)
        row[field+'_linear_final'] = float(last)
    cont = re.search(r'continuity errors : sum local = ([\d.eE+-]+), global = ([\d.eE+-]+), cumulative = ([\d.eE+-]+)', segment)
    if cont:
        row.update(dict(zip(['continuity_local','continuity_global','continuity_cumulative'], map(float, cont.groups()))))
    if 'p_initial' in row and row['iteration'] <= BEST_TIME:
        rows.append(row)
columns = list(rows[0])
with (OUT/'residuals.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

reader = OpenFOAMReader(FileName=str(CASE/'V00.foam'))
reader.MeshRegions = ['internalMesh']
reader.CellArrays = ['U', 'p', 'k', 'epsilon', 'nut']
reader.UpdatePipeline(time=float(final.name))
datasets = list(leaves(servermanager.Fetch(reader)))
assert len(datasets) == 1, [d.GetClassName() for d in datasets]
grid = datasets[0]
vol = sizes(grid, 'Volume')
u = vtk_to_numpy(grid.GetCellData().GetArray('U'))
p = vtk_to_numpy(grid.GetCellData().GetArray('p'))*RHO
speed = np.linalg.norm(u, axis=1)
centres = vtkCellCenters()
centres.SetInputData(grid)
centres.Update()
xyz = vtk_to_numpy(centres.GetOutput().GetPoints().GetData())
audit = json.loads((CASE/'geometry_audit.json').read_text())
assert abs(vol.sum()-audit['fluid_volume_m3']) < 1e-7
assert len(vol) == audit['total_cells']
assert np.isfinite(u).all() and np.isfinite(p).all() and (vol > 0).all()
q_in = patch_values(final/'phi', 'AIR_INLET')
q_out = patch_values(final/'phi', 'AIR_OUTLET')
q_wall = patch_values(final/'phi', 'WALLS', count=10092)
# AIR_INLET p uses zeroGradient — no boundary value is stored in the field file.
# Read the area-averaged kinematic pressure from the postProcessing function output.
_pp_dir = sorted((CASE/'postProcessing/inletPressure').iterdir(),
                 key=lambda d: float(d.name))[0]   # earliest restart dir covers t=0–3000
_pp_path_3k = CASE/'postProcessing/inletPressure/3000/surfaceFieldValue.dat'
if _pp_path_3k.exists():
    _pp = np.loadtxt(_pp_path_3k, comments='#')
    _idx = int(np.argmin(np.abs(_pp[:, 0] - BEST_TIME)))
    _p_in_kpa = float(_pp[_idx, 1])
else:
    _p_in_kpa = 27.499   # fallback from log
pin = np.full(len(q_in), _p_in_kpa * RHO)  # Pa, uniform over inlet faces
pout = patch_values(final/'p', 'AIR_OUTLET', count=len(q_out))*RHO
uin = patch_values(final/'U', 'AIR_INLET', 3, len(q_in))
uout = patch_values(final/'U', 'AIR_OUTLET', 3, len(q_out))
# Inlet uniform speed makes -phi equal each inlet face area in this case.
ain = -q_in
# Outlet block consists of identical 0.02 x (0.25/13) m faces.
aout = np.full(len(q_out), audit['boundary_area_m2']['AIR_OUTLET']/len(q_out))
assert len(q_out) == 325, 'Update outlet area weighting for a different mesh'
yp = patch_values(final/'yPlus', 'WALLS')
metrics = {
    'label':'SIMULATION — V00', 'case':str(CASE), 'final_iteration':float(final.name),
    'solved_iterations':len(rows), 'solver_reported_converged':bool(re.search(r'converged in \d+ iterations', log)),
    'last_residuals':rows[-1], 'fluid_volume_m3':float(vol.sum()), 'cell_count':len(vol),
    'flow_m3_s':{'inlet_outward_signed':float(q_in.sum()),'outlet_outward_signed':float(q_out.sum()),
                 'wall_signed':float(q_wall.sum()),'outlet_backflow':float(-q_out[q_out<0].sum())},
    'mass_imbalance_percent':float(abs(q_in.sum()+q_out.sum()+q_wall.sum())/-q_in.sum()*100),
    'mass_in_kg_s':float(-q_in.sum()*RHO),'mass_out_kg_s':float(q_out.sum()*RHO),
    'pressure_Pa':{'cell_min':float(p.min()),'cell_max':float(p.max()),
                   'volume_mean':float(np.average(p, weights=vol)),
                   'inlet_area_mean':float(np.average(pin, weights=ain)),
                   'outlet_area_mean':float(np.average(pout, weights=aout)),
                   'inlet_flux_weighted_total':float(np.average(pin+0.5*RHO*np.sum(uin**2,axis=1), weights=-q_in)),
                   'outlet_flux_weighted_total':float(np.average(pout+0.5*RHO*np.sum(uout**2,axis=1), weights=q_out))},
    'speed_m_s':{'cell_min':float(speed.min()),'cell_max':float(speed.max()),
                 'volume_mean':float(np.average(speed, weights=vol)), 'wall_boundary':0,
                 'max_cell_center_m':xyz[int(np.argmax(speed))].tolist()},
    'slow_volume_fraction_below_0p1_m_s':float(vol[speed<0.1].sum()/vol.sum()),
    'wall_yplus':{'min':float(yp.min()), 'max':float(yp.max()), 'face_mean':float(yp.mean()),
                  'face_fraction_below_30':float(np.mean(yp<30)), 'face_fraction_above_300':float(np.mean(yp>300))},
    'regions':{}, 'sections':{}, 'source_cad_sha256':audit['source_sha256'],
    'log_sha256_orig':hashlib.sha256((CASE/'logs/foamRun.log').read_bytes()).hexdigest(),
    'log_sha256_cont':hashlib.sha256((CASE/'logs/foamRun_continue.log').read_bytes()).hexdigest()
}
coverage = np.zeros(len(vol), dtype=int)
for name, item in audit['regions'].items():
    bounds = np.array(item['bounds_mm'])/1000
    mask = np.all((xyz > bounds[::2]) & (xyz < bounds[1::2]), axis=1)
    coverage += mask
    assert int(mask.sum()) == audit['cell_counts'][name]
    axis = 2 if name == 'CLEAN_RISER' else 0
    metrics['regions'][name] = {'cells':int(mask.sum()), 'volume_m3':float(vol[mask].sum()),
        'speed_volume_mean_m_s':float(np.average(speed[mask],weights=vol[mask])),
        'reverse_volume_fraction':float(vol[mask & (u[:,axis]<-0.05)].sum()/vol[mask].sum()),
        'reverse_definition':f'U{"xyz"[axis]} < -0.05 m/s; indicator, not a closed-vortex proof'}
assert (coverage == 1).all()
for name, origin, normal in [
    ('STAGE_01_mid', [0.165,0.4,0.5], [1,0,0]),
    ('STAGE_02_mid', [0.235,0.4,0.5], [1,0,0]),
    ('STAGE_03_mid', [0.305,0.4,0.5], [1,0,0]),
    ('riser_entry_above_turn', [0.4,0.4,0.86], [0,0,1]),
    ('riser_mid', [0.4,0.4,1.2], [0,0,1]),
    ('outlet_mid', [0.695,0.4,1.7], [1,0,0])]:
    plane = vtkPlane()
    plane.SetOrigin(origin)
    plane.SetNormal(normal)
    cut = vtkCutter()
    cut.SetCutFunction(plane)
    cut.SetInputData(grid)
    cut.Update()
    section = cut.GetOutput()
    area = sizes(section, 'Area')
    su = vtk_to_numpy(section.GetCellData().GetArray('U'))
    sp = vtk_to_numpy(section.GetCellData().GetArray('p'))*RHO
    smag = np.linalg.norm(su,axis=1)
    un = su @ np.array(normal)
    avg = float(np.average(un,weights=area))
    metrics['sections'][name] = {'origin_m':origin,'normal':normal,'area_m2':float(area.sum()),
        'speed_area_mean_m_s':float(np.average(smag,weights=area)),
        'normal_velocity_area_mean_m_s':avg,
        'normal_velocity_CoV':float(np.sqrt(np.average((un-avg)**2,weights=area))/abs(avg)),
        'pressure_area_mean_Pa':float(np.average(sp,weights=area)),
        'reverse_area_fraction':float(area[un<0].sum()/area.sum()),
        'sampled_volume_flow_m3_s':float(np.sum(un*area)),
        'method':'Piecewise cell values on VTK cut; not conservative face phi'}

# Use the postProcessing segment that covers the reference timestep (6000 from SIMPLEC run)
_pp3k = CASE/'postProcessing/inletPressure/3000/surfaceFieldValue.dat'
if _pp3k.exists():
    _history = np.loadtxt(_pp3k, comments='#')
    _late = _history[_history[:, 0] >= float(final.name) - 100]
    if len(_late) > 0:
        metrics['late_100_iteration_inlet_pressure_range_Pa'] = float(np.ptp(_late[:, -1]) * RHO)
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
print(json.dumps(metrics,indent=2))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9,4.5), layout='constrained')
styles = [('Ux','#3569a8','-'),('Uy','#3569a8','--'),('Uz','#3569a8',':'),
          ('p','#ae7927','-'),('k','#ae7927','--'),('epsilon','#ae7927',':')]
for field, color, style in styles:
    ax.semilogy([r['iteration'] for r in rows],[r[field+'_initial'] for r in rows],
                label=field,color=color,linestyle=style,linewidth=1.1)
ax.axhline(1e-5,color='grey',ls='--',lw=0.8,label='p criterion')
ax.axhline(1e-6,color='black',ls=':',lw=0.8,label='U/k/epsilon criterion')
ax.set(xlabel='Steady iteration (not physical seconds)',ylabel='Initial equation residual',
       title='SIMULATION — V00 | Residual history')
ax.grid(alpha=0.2)
ax.legend(ncol=4,fontsize=8)
fig.savefig(OUT/'residual_history.png',dpi=160)
plt.close(fig)

# ParaView uses the same final actual field data for the following images.
view = CreateView('RenderView')
view.ViewSize = [1100,950]
view.OrientationAxesVisibility = 1
view.Background = [1,1,1]
view.UseColorPaletteForBackground = 0
view.CameraParallelProjection = 1
view.CameraPosition = [0.35,-5,1.075]
view.CameraFocalPoint = [0.35,0.4,1.075]
view.CameraViewUp = [0,0,1]
view.CameraParallelScale = 1.09
view.ViewTime = float(final.name)
section = Slice(Input=reader)
section.SliceType = 'Plane'
section.SliceType.Origin = [0.35,0.4,1.075]
section.SliceType.Normal = [0,1,0]
section.UpdatePipeline(time=float(final.name))
display = Show(section,view)
ColorBy(display,('POINTS','U','Magnitude'))
lut = GetColorTransferFunction('U')
lut.ApplyPreset('Viridis (matplotlib)',True)
lut.RescaleTransferFunction(0,float(speed.max()))
display.SetScalarBarVisibility(view,True)
bar = GetScalarBar(lut,view)
bar.Title = 'Speed'
bar.ComponentTitle = 'm/s'
bar.TitleColor = [0,0,0]
bar.LabelColor = [0,0,0]
bar.ScalarBarLength = 0.5
streams = StreamTracer(Input=reader,SeedType='Line')
streams.Vectors = ['POINTS','U']
streams.SeedType.Point1 = [0.005,0.4,0.17]
streams.SeedType.Point2 = [0.005,0.4,0.83]
streams.SeedType.Resolution = 24
streams.MaximumStreamlineLength = 5
streams.IntegrationDirection = 'FORWARD'
stream_display = Show(streams,view)
ColorBy(stream_display,None)
stream_display.DiffuseColor = [0.05,0.05,0.05]
stream_display.LineWidth = 1.2
title = Text()
title.Text = 'SIMULATION — V00\nEmpty tower | speed + inlet-seeded streamlines\nCentral section Y = 0.400 m | PLACEHOLDER inlet: 1 m/s'
td = Show(title,view)
td.Color = [0,0,0]
td.FontSize = 14
td.WindowLocation = 'Upper Left Corner'
Render(view)
SaveScreenshot(str(OUT/'velocity_streamlines.png'),view,ImageResolution=[1100,950])
Hide(streams,view)
Hide(section,view)
display.SetScalarBarVisibility(view,False)
calc = Calculator(Input=section)
calc.ResultArrayName = 'pressure_Pa'
calc.Function = '1.2*p'
pd = Show(calc,view)
ColorBy(pd,('POINTS','pressure_Pa'))
plut = GetColorTransferFunction('pressure_Pa')
plut.ApplyPreset('Cool to Warm (Extended)',True)
plut.RescaleTransferFunction(float(p.min()),float(p.max()))
pd.SetScalarBarVisibility(view,True)
pbar = GetScalarBar(plut,view)
pbar.Title = 'Gauge pressure'
pbar.ComponentTitle = 'Pa'
pbar.TitleColor = [0,0,0]
pbar.LabelColor = [0,0,0]
pbar.ScalarBarLength = 0.5
title.Text = 'SIMULATION — V00\nEmpty tower | flow-induced gauge pressure\nCentral section Y = 0.400 m | outlet reference: 0 Pa'
Render(view)
SaveScreenshot(str(OUT/'pressure_section.png'),view,ImageResolution=[1100,950])
SaveState(str(OUT/'V00_inspection.pvsm'))
