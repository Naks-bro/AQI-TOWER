# Indoor particle room model - 5 October 2026

ASSUMPTIONS: well-mixed closed room, constant size-specific particle-clean-air delivery, no ongoing source/outdoor influx; natural deposition and ventilation excluded. Scene person1.70 m is a scale marker only. Room is drawn square from adjustable floor area; height is independently adjustable. These are not measured premises or an occupied-room simulation. Default25 m2,2.8 m,150 m3/h CADR are examples; D01 CADR is UNKNOWN.

V=area*height; concentration ratio=exp(-CADR*t_minutes/(60*V)); target time=-60*V*ln(1-reduction)/CADR. At zero CADR the modeled fraction stays1 and target time is unavailable. Exactly100% removal is not reached in finite ideal time. The plot shows relative particles, not AQI or disease risk.

Example25 m2/2.8 m/150 m3/h:90% in64.472 min. Double volume doubles time; double clean-air rate halves it. To reach90% in30 min,70 m3 requires322.362 m3/h CADR. If filtration airflow were300 m3/h and capture perfect, minimum ideal time would be32.236 min; both actual airflow and capture remain unmeasured. User-entered rates above300 do not describe that300 m3/h screening point.

Targets: airborne dust and fine smoke particles, with PM2.5/PM10 trial measurements proposed. No whole-device HEPA, gases/CO2/CO/VOCs/odours, bacteria/virus control, medical protection or outdoor coverage established. Filtration supplements source control and ventilation; no intentional ozone, ionizer or UV stage is added.

Sources checked5 October2026:
- EPA https://www.epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home : CADR is particle-specific, room volume matters, gas removal is distinct, filtration does not replace ventilation/source control. EPA does not certify D01.
- CDC https://www.cdc.gov/infection-control/hcp/environmental-control/appendix-b-air.html : ideal exponential purge equation and no-source/perfect-mixing limits. We adapt Q to effective particle clean-air delivery; this is NOT healthcare clearance advice or certification.

Existing research analysis: engineering/scripts/analysis/indoor_decay.py. It consumes recorder CSV fields timestamp_utc,stage,run_id,evidence_kind,channel,instrument_id,value,unit,calibration_reference. A plan specifies actual run/channel/instrument, indoor environment, room_volume_m3 and measured/assumed basis, usable_pm_floor_ug_m3 and floor evidence, off/on time windows and explicit assumption declarations. Run its --help and eight synthetic tests; never turn a synthetic fixture into physical evidence. This analysis does not subtract an asymptotic background, evaluate repeatability or produce confidence intervals. Use expert-designed real trials after safe commissioning; do not generate smoke or contaminants for a stakeholder demo.

Remaining engineering release register is unchanged: source data, guard/structure/seals, rated circuit/enclosure, commissioning and physical trials remain OPEN. This supplement closes the room-scenario software task, not those approvals.
