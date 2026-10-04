"""R03M pressure screening and strict airflow-data arithmetic; no safety approval."""
import argparse, csv, hashlib, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def finite(value, name, positive=False):
    try: x=float(value)
    except (ValueError,TypeError): raise ValueError(name+': missing/non-numeric')
    if not math.isfinite(x) or x<0 or (positive and x==0):
        raise ValueError(name+': invalid range')
    return x

def pressure_rows():
    curve=ROOT/'reports/prototype_d01/component_validation/OEM_P14_Max_points.csv'
    guard=ROOT/'reports/prototype_d01/mechanical_package/guard_pattern.json'
    pts=[(float(r['single_fan_m3h']),float(r['static_Pa'])) for r in csv.DictReader(curve.open())]
    area=json.loads(guard.read_text())['hole_area_m2']
    rows=[]
    for q in (200,250,300,350,400):
        x=q/4
        a,b,c,d=next((a,b,c,d) for (a,b),(c,d) in zip(pts,pts[1:]) if a<=x<=c)
        available=b+(d-b)*(x-a)/(c-a)
        for k in (.5,1,2):
            v=q/3600; fanarea=4*math.pi*(.1342/2)**2
            terms={'plenum_Pa':1.5*.6*(v/fanarea)**2,
                   'inner_guard_Pa':1.5*.6*(v/area)**2,
                   'outer_guard_Pa':1.5*.6*(v/area)**2,
                   'installation_Pa':.6*(v/fanarea)**2,
                   'reducer_Pa':k*.6*(v/2/.0945)**2}
            rows.append(dict(total_m3h=q,per_filter_m3h=q/2,reducer_K=k,
                             fan_Pa=available,**terms,nonfilter_Pa=sum(terms.values()),
                             filter_allowance_Pa=available-sum(terms.values())))
    return {'status':'CONDITIONAL SCREEN - NOT ACTUAL FLOW', 'geometry':'R03M',
      'guard_open_area_each_m2':area,
      'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (curve,guard)},
      'assumptions':'2800 rpm OEM numeric curve; equal sharing among four fans and two parallel filters; density1.2; guard K1.5 each; plenum K1.5 and installation K1 on fan-aperture velocity. Reducer K0.5/1/2. Loss coefficients unverified; reducer/plenum may overlap. Static/installed compatibility unresolved. No loaded filter curve.',
      'rows':rows}

def airflow(rows):
    """Area-weighted positive normal velocities, one plane/run. Reject incomplete records."""
    if len(rows)<4:raise ValueError('At least four cells required; this does not establish sufficient sampling.')
    parsed=[]; ids=set(); conditions=set()
    for r in rows:
        for key in ('run_id','cell_id','instrument_id','calibration_ref','method_ref','assembly_revision','timestamp'):
            if not str(r.get(key,'')).strip():raise ValueError('Missing '+key)
        if r.get('evidence')!='PHYSICAL':raise ValueError('Physical evidence label required; templates/synthetic rows refused')
        if r.get('quality')!='ACCEPTED':raise ValueError('Reviewer acceptance missing')
        conditions.add((r['run_id'],r['instrument_id'],r['assembly_revision'],r['method_ref']))
        if r['cell_id'] in ids:raise ValueError('Duplicate cell ID')
        ids.add(r['cell_id'])
        area=finite(r.get('cell_area_m2'),'area',True)
        v=finite(r.get('normal_velocity_ms'),'normal velocity')
        u=finite(r.get('velocity_error_bound_ms'),'velocity error bound')
        parsed.append((area,v,u))
    if len(conditions)!=1:raise ValueError('Do not mix runs, instruments, revisions or methods')
    q=3600*sum(a*v for a,v,u in parsed)
    bound=3600*sum(a*u for a,v,u in parsed)
    return {'status':'ARITHMETIC ONLY - reviewer must validate method and uncertainty',
      'run_id':rows[0]['run_id'],'total_flow_m3h':q,'sampled_area_m2':sum(a for a,v,u in parsed),
      'velocity_only_flow_error_bound_m3h':bound,
      'lower_velocity_only_bound_m3h':max(0,q-bound),
      'omitted_uncertainties':'Area, swirl, blockage, spatial coverage, fixture leakage/loading, temporal variation and instrument correlation. Not a complete uncertainty budget.',
      'claim_limits':'No CADR, particle efficiency, HEPA class, safety or outdoor coverage from airflow alone.'}

def selftest():
    base={'run_id':'SYNTHETIC_TEST','instrument_id':'TEST','calibration_ref':'TEST',
      'method_ref':'TEST','assembly_revision':'TEST','timestamp':'TEST','evidence':'PHYSICAL','quality':'ACCEPTED',
      'cell_area_m2':.01,'normal_velocity_ms':2,'velocity_error_bound_ms':.1}
    # PHYSICAL token exercises parser only; never exported as measured data.
    rows=[dict(base,cell_id=str(i)) for i in range(4)]
    assert abs(airflow(rows)['total_flow_m3h']-288)<1e-9
    assert abs(airflow(rows)['velocity_only_flow_error_bound_m3h']-14.4)<1e-9
    n=2
    for field,value in [('normal_velocity_ms','nan'),('normal_velocity_ms',-1),('cell_area_m2',0),
        ('calibration_ref',''),('evidence','SYNTHETIC'),('quality',''),('velocity_error_bound_ms','')]:
        bad=[dict(r) for r in rows];bad[0][field]=value
        try:airflow(bad)
        except ValueError:n+=1
        else:raise AssertionError(field)
    for bad in (rows[:1],rows+[rows[0]],[dict(r,run_id=str(i)) for i,r in enumerate(rows)]):
        try:airflow(bad)
        except ValueError:n+=1
        else:raise AssertionError('invalid rows accepted')
    p=pressure_rows();assert len(p['rows'])==15;n+=1
    assert all(abs(r['fan_Pa']-r['nonfilter_Pa']-r['filter_allowance_Pa'])<1e-9 for r in p['rows']);n+=1
    assert p['guard_open_area_each_m2']<.036;n+=1
    return {'passed':n,'evidence':'SYNTHETIC / ARITHMETIC ONLY','physical_tests':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--airflow-csv',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    result=airflow(list(csv.DictReader(a.airflow_csv.open(encoding='utf-8-sig')))) if a.airflow_csv else selftest()
    if a.output:
        with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
