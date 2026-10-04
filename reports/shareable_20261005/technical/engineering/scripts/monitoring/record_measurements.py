"""Offline measurement importer. No sensor driver, fan control or safety function."""
import argparse
import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path

CHANNELS = {
    'pm25_room_a': ('ug/m3', 0, None),
    'pm25_room_b': ('ug/m3', 0, None),
    'dp_prefilter': ('Pa', None, None),
    'dp_hepa': ('Pa', None, None),
    'airflow': ('m3/h', 0, None),
    'power': ('W', 0, None),
    'temperature': ('degC', None, None),
    'humidity': ('percent', 0, 100),
    'noise': ('dBA', None, None),
}
FIELDS = ['timestamp_utc', 'run_id', 'evidence_kind', 'stage', 'channel',
          'value', 'unit', 'instrument_id', 'calibration_reference', 'notes']


def known(value):
    return isinstance(value, str) and value.strip().upper() not in ('', 'UNKNOWN', 'UNSET')


def validate_metadata(meta):
    if not known(meta.get('run_id')):
        raise ValueError('Set a real run_id; do not use UNSET')
    if meta.get('evidence_kind') not in ('physical_measurement', 'synthetic_test'):
        raise ValueError('Explicit physical_measurement or synthetic_test required')
    if not isinstance(meta.get('instruments'), dict) or not meta['instruments']:
        raise ValueError('Register the instruments first')
    for identity, instrument in meta['instruments'].items():
        if not known(identity) or not isinstance(instrument, dict):
            raise ValueError('Invalid instrument identity')
        if instrument.get('channel') not in CHANNELS:
            raise ValueError('Instrument must have one supported channel')
        if not known(instrument.get('position_or_method')):
            raise ValueError('Record position or measurement method')
        if meta['evidence_kind'] == 'physical_measurement' and not known(instrument.get('model')):
            raise ValueError('Physical data needs an identified instrument model')
    return meta


def validate_record(record, meta):
    if set(record) != {'timestamp', 'stage', 'channel', 'value', 'unit', 'instrument_id', 'notes'}:
        raise ValueError('Record fields must match the documented input schema')
    stamp = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError('Timestamp must include its UTC offset')
    channel = record['channel']
    if channel not in CHANNELS:
        raise ValueError('Unsupported channel')
    unit, lower, upper = CHANNELS[channel]
    value = record['value']
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Reading must be a finite number; omit missing readings')
    if (lower is not None and value < lower) or (upper is not None and value > upper):
        raise ValueError('Reading outside basic validity limits; no sensor-range guarantee')
    if record['unit'] != unit:
        raise ValueError('Wrong unit; convert explicitly before importing')
    instrument = meta['instruments'].get(record['instrument_id'])
    if instrument is None or instrument['channel'] != channel:
        raise ValueError('Channel/instrument mismatch')
    if record['stage'] not in ('colocation', 'baseline_off', 'tower_on', 'postcheck'):
        raise ValueError('Unsupported research stage')
    if not isinstance(record['notes'], str):
        raise ValueError('Notes must be text')
    return {
        'timestamp_utc': stamp.astimezone(timezone.utc).isoformat(),
        'run_id': meta['run_id'], 'evidence_kind': meta['evidence_kind'],
        'stage': record['stage'], 'channel': channel, 'value': value,
        'unit': unit, 'instrument_id': record['instrument_id'],
        'calibration_reference': instrument.get('calibration_reference') or 'UNKNOWN',
        'notes': record['notes'],
    }


def import_readings(metadata_path, input_path, output_path):
    meta = validate_metadata(json.loads(Path(metadata_path).read_text(encoding='utf-8')))
    rows, seen, latest = [], set(), {}
    for number, line in enumerate(Path(input_path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = validate_record(json.loads(line), meta)
            key = (row['instrument_id'], row['timestamp_utc'])
            if key in seen:
                raise ValueError('Duplicate instrument/timestamp')
            if row['instrument_id'] in latest and row['timestamp_utc'] < latest[row['instrument_id']]:
                raise ValueError('Out-of-order time for this instrument')
            seen.add(key)
            latest[row['instrument_id']] = row['timestamp_utc']
            rows.append(row)
        except (ValueError, TypeError, KeyError, AttributeError) as error:
            raise ValueError(f'Input line {number}: {error}') from error
    if not rows:
        raise ValueError('No readings: no measurement file produced')
    # Validate all input first; never append to or overwrite an existing evidence file.
    with Path(output_path).open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata', required=True)
    parser.add_argument('--input', required=True, help='JSON Lines readings, one actual reading per line')
    parser.add_argument('--output', required=True, help='New CSV file; parent directory must exist')
    args = parser.parse_args()
    try:
        count = import_readings(args.metadata, args.input, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f'Not imported: {error}\n')
    print(f'Imported {count} readings. No calibration, safety or performance approval implied.')


if __name__ == '__main__':
    main()
