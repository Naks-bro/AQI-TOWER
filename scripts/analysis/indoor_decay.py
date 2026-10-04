"""Exploratory single-pair indoor particle decay; never certified CADR."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path


def stamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Timestamp needs UTC offset')
    return result.astimezone(timezone.utc)


def number(value, minimum=0):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a numeric input')
    result = float(value)
    if not math.isfinite(result) or result < minimum:
        raise ValueError('Nonfinite or out-of-range input')
    return result


def fit_decay(points, floor):
    floor = number(floor)
    if len(points) < 5:
        raise ValueError('At least five readings per window required by this tool')
    times = [stamp(p[0]) for p in points]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('Duplicate or backwards timestamps in window')
    values = [number(p[1]) for p in points]
    if any(v <= floor for v in values):
        raise ValueError('Reading at/below supplied usable floor; no clipping or dropping')
    x = [(t - times[0]).total_seconds() / 3600 for t in times]
    y = [math.log(v) for v in values]
    xm, ym = sum(x) / len(x), sum(y) / len(y)
    xx = sum((v - xm) ** 2 for v in x)
    slope = sum((a - xm) * (b - ym) for a, b in zip(x, y)) / xx
    if not math.isfinite(slope):
        raise ValueError('Numerically invalid fit')
    intercept = ym - slope * xm
    residuals = [b - (intercept + slope * a) for a, b in zip(x, y)]
    sse = sum(r * r for r in residuals)
    yy = sum((v - ym) ** 2 for v in y)
    return {'samples': len(x), 'duration_h': x[-1], 'decay_rate_per_h': -slope,
            'r_squared': None if yy == 0 else 1 - sse / yy,
            'log_residuals': residuals, 'relative_times_h': x,
            'first_utc': times[0].isoformat(), 'last_utc': times[-1].isoformat()}


def analyze(rows, plan):
    if plan.get('environment') != 'indoor':
        raise ValueError('Indoor only: no outdoor decay estimate')
    if plan.get('channel') not in ('pm25_room_a', 'pm25_room_b'):
        raise ValueError('Select a supported room particle channel')
    if plan.get('volume_basis') not in ('measured', 'assumed'):
        raise ValueError('Volume basis must be explicit')
    volume = number(plan['room_volume_m3'])
    if volume <= 0:
        raise ValueError('Room volume must be positive')
    floor = number(plan['usable_pm_floor_ug_m3'])
    if not rows:
        raise ValueError('No input data')
    kinds = {r['evidence_kind'] for r in rows}
    run_ids = {r['run_id'] for r in rows}
    if len(kinds) != 1 or not kinds <= {'physical_measurement', 'synthetic_test'}:
        raise ValueError('Mixed or unknown evidence kinds')
    if run_ids != {plan.get('run_id')} or plan.get('run_id') in (None, '', 'UNSET', 'UNKNOWN'):
        raise ValueError('Exactly one identified matching run required')
    if kinds == {'physical_measurement'} and floor <= 0:
        raise ValueError('Physical readings require a documented positive usable floor')
    if kinds == {'physical_measurement'} and plan.get('floor_evidence_reference') in (None, '', 'UNKNOWN', 'UNSET'):
        raise ValueError('Document the usable-floor evidence reference')
    windows, intervals, selected = {}, [], []
    for stage in ('baseline_off', 'tower_on'):
        start, end = (stamp(plan[stage][k]) for k in ('start', 'end'))
        if end <= start:
            raise ValueError('Invalid analysis window')
        intervals.append((start, end))
        subset = [r for r in rows if r['channel'] == plan['channel']
                  and r['instrument_id'] == plan['instrument_id']
                  and start <= stamp(r['timestamp_utc']) <= end]
        if any(r['stage'] != stage or r['unit'] != 'ug/m3' for r in subset):
            raise ValueError('Selected window includes wrong stage or unit')
        windows[stage] = fit_decay([(r['timestamp_utc'], r['value']) for r in subset], floor)
        selected.extend(subset)
    if max(i[0] for i in intervals) <= min(i[1] for i in intervals):
        raise ValueError('Off/on windows overlap')
    difference = windows['tower_on']['decay_rate_per_h'] - windows['baseline_off']['decay_rate_per_h']
    declarations = ('well_mixed_assumption', 'matched_ventilation_declared', 'stable_sources_declared')
    ready = all(plan.get(k) is True for k in declarations)
    warnings = ['Single pair only; repeatability and measurement uncertainty NOT evaluated.',
                'No confidence interval or significance claim; correlated samples and instrument drift require review.',
                'No background-asymptote correction; model requires negligible influx/background relative to readings.',
                'R-squared and declared conditions do not verify well-mixed behavior or matched ventilation.',
                'Research diagnostic only; not certified CADR, filter integrity, health benefit or outdoor coverage.']
    if not ready:
        warnings.append('Required model assumptions not declared; clean-air-flow estimate withheld.')
    if difference <= 0:
        warnings.append('No positive additional decay in selected pair; do not claim improvement.')
    if any(w['decay_rate_per_h'] < 0 for w in windows.values()):
        warnings.append('Particles increased in a selected window; simple decay model needs review.')
    if any(r.get('calibration_reference') in (None, '', 'UNKNOWN') for r in selected):
        warnings.append('Selected readings lack calibration reference; accuracy unverified.')
    if plan['volume_basis'] == 'assumed':
        warnings.append('Assumed room volume: any estimate is a hypothetical scenario.')
    return {'status': 'EXPLORATORY ONLY — NO PERFORMANCE PASS/FAIL',
            'evidence_kind': next(iter(kinds)), 'run_id': plan['run_id'],
            'channel': plan['channel'], 'instrument_id': plan['instrument_id'],
            'room_volume_m3': volume, 'volume_basis': plan['volume_basis'],
            'usable_pm_floor_ug_m3': floor, 'windows': windows,
            'additional_decay_per_h': difference,
            'conditional_clean_air_flow_m3h': volume * difference if ready else None,
            'assumption_declarations': {k: plan.get(k) is True for k in declarations},
            'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='Recorder CSV for one run')
    parser.add_argument('--plan', required=True, help='Explicit windows, instrument, floor, volume and assumptions')
    parser.add_argument('--output', required=True, help='New JSON file; never overwrites')
    args = parser.parse_args()
    try:
        source = Path(args.input)
        plan_path = Path(args.plan)
        with source.open(newline='', encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
        result = analyze(rows, json.loads(plan_path.read_text(encoding='utf-8')))
        result['provenance'] = {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (source, plan_path)}
        with Path(args.output).open('x', encoding='utf-8') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\n')
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, f'Not analyzed: {error}\n')
    print('Exploratory analysis saved; read warnings before interpretation.')


if __name__ == '__main__':
    main()
