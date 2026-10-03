"""Current R02G pressure allowance; unknown filter remains an unknown, not a fitted curve."""
import csv,json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/current_handoff'
source=R/'reports/prototype_d01/component_validation/OEM_P14_Max_points.csv'
pts=[(float(r['single_fan_m3h']),float(r['static_Pa'])) for r in csv.DictReader(source.open())]
def fan(q):
    x=q/4
    if not 0<=x<=pts[-1][0]:raise ValueError('Outside OEM numeric curve; extrapolation refused')
    for (a,b),(c,d) in zip(pts,pts[1:]):
        if a<=x<=c:return b+(d-b)*(x-a)/(c-a)
    raise ValueError(x)
def budget(q,k):
    if q<0 or k<0:raise ValueError('Negative flow/loss coefficient')
    rho=1.2;f=q/3600
    fan_area=4*math.pi*(.1342/2)**2;guard_area=.300*.300*.4
    inlet_area=.350*.270 # each of TWO parallel filter openings
    dp=lambda v:rho*v*v/2
    return dict(plenum_Pa=1.5*dp(f/fan_area),inner_guard_Pa=1.5*dp(f/guard_area),
        outer_guard_Pa=1.5*dp(f/guard_area),installation_allowance_Pa=dp(f/fan_area),
        reducer_path_Pa=k*dp((f/2)/inlet_area))
rows=[]
for q in (200,250,300,350,400):
    for k in (.5,1.,2.):
        b=budget(q,k);rows.append(dict(total_m3h=q,each_filter_m3h=q/2,assumed_reducer_K=k,
            fan_available_Pa=fan(q),**b,nonfilter_total_Pa=sum(b.values()),filter_allowance_Pa=fan(q)-sum(b.values())))
tests=dict(parallel_flow_not_pressure=abs(fan(4*pts[5][0])-pts[5][1])<1e-9,
    zero_losses=sum(budget(0,1).values())==0,
    quadratic_losses=all(abs(budget(400,1)[k]-4*v)<1e-9 for k,v in budget(200,1).items()),
    reducer_path_not_series=abs(budget(360,1)['reducer_path_Pa']-.6*(.05/.0945)**2)<1e-10,
    budget_closure=all(abs(r['fan_available_Pa']-r['nonfilter_total_Pa']-r['filter_allowance_Pa'])<1e-9 for r in rows),
    pressure_decreases_with_flow=all(fan(a)>fan(b) for a,b in zip((200,250,300,350),(250,300,350,400))),
    higher_loss_reduces_allowance=all(rows[i]['filter_allowance_Pa']>rows[i+1]['filter_allowance_Pa']>rows[i+2]['filter_allowance_Pa'] for i in range(0,15,3)))
try:fan(4*pts[-1][0]+1)
except ValueError:tests['no_extrapolation']=True
else:tests['no_extrapolation']=False
assert all(tests.values())
data=dict(status='CONDITIONAL PRESSURE ALLOWANCE - NOT PREDICTED OR MEASURED FLOW',geometry='R02G',
    curve_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    OEM_url='https://support.arctic.de/products/p14-max/techdocs/P14%20Max%20-%20PQ%20Curve%20for%20CFD.XLSX',
    assumptions='Full2800rpm, equal parallel sharing, rho1.2, no bypass, 40% guard porosity over300mm square; K values and installation allowance unverified. Reducer term is added conservatively to existing plenum allowance and may overlap its losses. Static/installed pressure compatibility unresolved.',
    unknowns='Actual filter clean/loaded curve, seal bypass, installed fan curve, guard loss and operating flow; no guaranteed margin. No CADR or outdoor coverage.',
    rows=rows,tests=tests)
O.mkdir(exist_ok=True);(O/'CURRENT_PRESSURE_BUDGET.json').write_text(json.dumps(data,indent=2))
with (O/'CURRENT_PRESSURE_BUDGET.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(dict(tests=tests,central_K1=[r for r in rows if r['assumed_reducer_K']==1]),indent=2))
