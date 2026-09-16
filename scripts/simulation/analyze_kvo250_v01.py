"""Extract traceable KVO 250 V01 metrics and render actual fields with WSL pvpython.

Usage: pvpython --force-offscreen-rendering analyze_kvo250_v01.py [case-directory]
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
CASE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT/'cfd/V01_fan'
OUT = ROOT/'results/CFD_V01_FAN'
OUT.mkdir(parents=True, exist_ok=True)
RHO = 1.20


def patch_values(path, patch, components=1, count=None):
    text = path.read_text()
    match = re.search(r'\b'+re.escape(patch)+r'\s*\{', text, re.S)
    if not match:
        raise ValueError(f'Missing patch {patch} in {path}')
    start = match.end()
    depth = 1
    end = start
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    body = text[start:end-1]
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


log = (CASE/'logs/foamRun_kvo.log').read_text()
if (CASE/'logs/foamRun_kvo_continue.log').exists():
    log += '\n' + (CASE/'logs/foamRun_kvo_continue.log').read_text()
if not re.search(r'\nEnd\s*$', log):
    raise RuntimeError('KVO solver has not ended cleanly')
times = sorted((p for p in CASE.iterdir() if p.is_dir() and re.fullmatch(r'\d+(?:\.\d+)?', p.name)
                and float(p.name) > 0), key=lambda p: float(p.name))
final = times[-1]
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
    if 'p_initial' in row:
        rows.append(row)
columns = list(rows[0])
with (OUT/'residuals.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

reader = OpenFOAMReader(FileName=str(CASE/'V01.foam'))
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
pin = patch_values(final/'p', 'AIR_INLET', count=len(q_in))*RHO
pout = patch_values(final/'p', 'AIR_OUTLET', count=len(q_out))*RHO
uin = patch_values(final/'U', 'AIR_INLET', 3, len(q_in))
uout = patch_values(final/'U', 'AIR_OUTLET', 3, len(q_out))
patch_reader = OpenFOAMReader(FileName=str(CASE/'V01.foam'))
available = list(patch_reader.MeshRegions.Available)
inlet_name = next(s for s in available if s.split('/')[-1] == 'AIR_INLET')
patch_reader.MeshRegions = [inlet_name]
patch_reader.UpdatePipeline(time=float(final.name))
inlet_grid = list(leaves(servermanager.Fetch(patch_reader)))[0]
ain = sizes(inlet_grid, 'Area')
assert len(ain) == len(pin) and abs(ain.sum()-0.42) < 1e-7
# Outlet block consists of identical 0.02 x (0.25/13) m faces.
aout = np.full(len(q_out), audit['boundary_area_m2']['AIR_OUTLET']/len(q_out))
assert len(q_out) == 325, 'Update outlet area weighting for a different mesh'
yp = patch_values(final/'yPlus', 'WALLS')
metrics = {
    'label':'SIMULATION — V01 | SYSTEMAIR KVO 250 | EMPTY TOWER | GRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES',
    'case':str(CASE), 'final_iteration':float(final.name),
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
    'log_sha256':hashlib.sha256(log.encode()).hexdigest()
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
        'normal_velocity_min_m_s':float(un.min()),
        'normal_velocity_max_m_s':float(un.max()),
        'normal_velocity_CoV':float(np.sqrt(np.average((un-avg)**2,weights=area))/abs(avg)),
        'pressure_area_mean_Pa':float(np.average(sp,weights=area)),
        'reverse_area_fraction':float(area[un<0].sum()/area.sum()),
        'sampled_volume_flow_m3_s':float(np.sum(un*area)),
        'method':'Piecewise cell values on VTK cut; not conservative face phi'}

fan = json.loads((ROOT/'data/fans/systemair_KVO_250.json').read_text())
curve_q = np.array([point['Q_m3s'] for point in fan['fan_curve_points']])
curve_p = np.array([point['delta_P_static_Pa'] for point in fan['fan_curve_points']])
Q = float(q_out.sum())
fan_head = float(np.interp(Q,curve_q,curve_p))
total_suction = metrics['pressure_Pa']['outlet_flux_weighted_total']
metrics['fan'] = {'Q_m3_s':Q,'Q_m3_h':Q*3600,'curve_static_Pa':fan_head,
    'measured_static_equivalent_Pa':-total_suction,
    'curve_closure_error_Pa':-total_suction-fan_head,
    'inside_source_curve':bool(curve_q[0]<Q<curve_q[-1]),
    'source_json_sha256':hashlib.sha256((ROOT/'data/fans/systemair_KVO_250.json').read_bytes()).hexdigest()}
metrics['pressure_Pa']['tower_static_difference'] = metrics['pressure_Pa']['inlet_area_mean']-metrics['pressure_Pa']['outlet_area_mean']
metrics['pressure_Pa']['tower_flux_weighted_total_loss'] = metrics['pressure_Pa']['inlet_flux_weighted_total']-total_suction
for monitor, factor in [('inletPressure',RHO),('outletFlow',1.0)]:
    history = np.vstack([np.atleast_2d(np.loadtxt(f)) for f in (CASE/'postProcessing'/monitor).glob('*/*.dat')])
    history = history[np.argsort(history[:,0])]
    late = history[(history[:,0]>=float(final.name)-100)&(history[:,0]<=float(final.name))]
    metrics[monitor+'_late100'] = {'min':float(late[:,-1].min()*factor),
        'max':float(late[:,-1].max()*factor),'range_percent_of_mean':float(np.ptp(late[:,-1])/abs(late[:,-1].mean())*100)}
metrics['criteria'] = {'residuals':all(rows[-1][f+'_initial'] < (1e-5 if f=='p' else 1e-6)
                        for f in ['p','Ux','Uy','Uz','k','epsilon']),
    'mass':metrics['mass_imbalance_percent'] < 0.1,
    'flow_stability':metrics['outletFlow_late100']['range_percent_of_mean'] < 0.1,
    'fan_closure':abs(metrics['fan']['curve_closure_error_Pa']) < 0.1}
v00 = json.loads((ROOT/'results/CFD_V00/metrics.json').read_text())
metrics['V00_comparison'] = {'reference_iteration':v00['final_iteration'],
    'flow_change_percent':(Q/0.42-1)*100,
    'max_speed_change_percent':(float(speed.max())/v00['speed_m_s']['cell_max']-1)*100,
    'V00_status':'PARTIAL — NON-CONVERGED; imposed flow'}
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
       title='SIMULATION — V01 | SYSTEMAIR KVO 250 | EMPTY TOWER\nResidual history | GRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES')
ax.grid(alpha=0.2)
ax.legend(ncol=4,fontsize=8)
fig.savefig(OUT/'residual_history.png',dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9,5),layout='constrained')
unc = np.array([pt.get('delta_P_uncertainty_Pa',0) for pt in fan['fan_curve_points']])
ax.plot(curve_q*3600,curve_p,'o-',color='#3569a8',label='Supplied six-point fan-static curve')
ax.errorbar(curve_q*3600,curve_p,yerr=unc,fmt='none',ecolor='#3569a8',capsize=4)
ax.scatter([Q*3600],[-total_suction],marker='D',s=55,c='#ae7927',zorder=5,label='Actual CFD operating point')
ax.annotate(f'{Q*3600:.1f} m³/h\n{-total_suction:.2f} Pa',xy=(Q*3600,-total_suction),
            xytext=(830,130),textcoords='data',arrowprops={'arrowstyle':'->'})
# A local Q² guide through the simulated resistance is NOT a multi-flow CFD sweep.
guide=np.linspace(0,curve_q[-1],100)
ax.plot(guide*3600,(-total_suction)*(guide/Q)**2,':',color='#555555',
        label='Q² resistance guide through this CFD point (not a sweep)')
ax.set(xlabel='Volume flow (m³/h)',ylabel='Fan-static-equivalent pressure (Pa)',ylim=(0,740),
    title='SIMULATION — V01 | SYSTEMAIR KVO 250 | EMPTY TOWER\nGRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES')
ax.grid(alpha=0.2)
ax.legend(fontsize=8)
fig.savefig(OUT/'fan_curve_operating_point.png',dpi=160)
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
view.CameraParallelScale = 1.22
view.OrientationAxesLabelColor = [0,0,0]
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
title.Text = 'SIMULATION — V01\nSYSTEMAIR KVO 250 / EMPTY TOWER\nGRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES\nSpeed + inlet-seeded streamlines; Y = 0.400 m; partial convergence'
td = Show(title,view)
td.Color = [0,0,0]
td.FontSize = 12
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
title.Text = 'SIMULATION — V01\nSYSTEMAIR KVO 250 / EMPTY TOWER\nGRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES\nGauge pressure; Y = 0.400 m; ambient reference = 0 Pa; partial convergence'
Render(view)
SaveScreenshot(str(OUT/'pressure_section.png'),view,ImageResolution=[1100,950])
SaveState(str(OUT/'V01_inspection.pvsm'))
Hide(calc,view)
pd.SetScalarBarVisibility(view,False)
stage = Slice(Input=reader)
stage.SliceType = 'Plane'
stage.SliceType.Origin = [0.305,0.4,0.5]
stage.SliceType.Normal = [1,0,0]
stage.UpdatePipeline(time=float(final.name))
sd = Show(stage,view)
ColorBy(sd,('POINTS','U','X'))
lut.ApplyPreset('Cool to Warm (Extended)',True)
lo=metrics['sections']['STAGE_03_mid']['normal_velocity_min_m_s']
hi=metrics['sections']['STAGE_03_mid']['normal_velocity_max_m_s']
extent=max(abs(lo),abs(hi))
lut.RescaleTransferFunction(-extent,extent)
sd.SetScalarBarVisibility(view,True)
bar.Title='Normal velocity'
bar.ComponentTitle='Ux (m/s)'
view.CameraPosition=[-4,0.4,0.5]
view.CameraFocalPoint=[0.305,0.4,0.5]
view.CameraViewUp=[0,0,1]
view.CameraParallelScale=0.47
title.Text='SIMULATION — V01\nSYSTEMAIR KVO 250 / EMPTY TOWER\nGRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES\nEMPTY STAGE_03 at X = 0.305 m; negative Ux = reverse flow; partial convergence'
Render(view)
SaveScreenshot(str(OUT/'stage03_cross_section.png'),view,ImageResolution=[1100,950])
