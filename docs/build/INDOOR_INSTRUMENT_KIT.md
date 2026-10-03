# Practical equipment for the first indoor test

3 October 2026. RECOMMENDATION / OEM REFERENCE CHECK — NOT AN ORDER OR WIRING RELEASE.

## Simple decision

USER UPDATE: no college lab is available; college/NGO provide funding only. Follow [the no-lab route](NO_LAB_BUILD_ROUTE.md): buy monitoring instruments, rent specialist equipment or hire an equipped test service. Start with the existing laptop; no custom PCB, wireless dashboard or extra computer is necessary for the current offline recorder.

Use [the revised equipment request sheet](INDOOR_INSTRUMENT_REQUEST_NO_LAB.csv) to record actual models, calibration, availability and interfaces. All availability/prices remain UNKNOWN. Quantities below are proposed test arrangements, not approved purchases. The older college-based CSV could not be overwritten and is retained as superseded history; use this new revision.

| Measurement | Proposed first arrangement | Buy/rent/service route | What must be confirmed |
|---|---|---|---|
| Room PM2.5 trend | Two matched logging monitors, at two recorded room positions | Buy complete supported instruments/kits; see no-lab route | Export format, co-location checks, usable floor, uncertainty and humidity response |
| Prefilter and HEPA pressure loss | Two simultaneous signed differential-pressure channels | Buy calibrated manometer/logger or rent for commissioning; digital modules optional | Clean/loaded/fault range, reference check, tubing and tap installation |
| Actual whole-tower airflow | Calibrated capture hood or reviewed duct-traverse setup | Hire equipped service or rent with experienced operator | Outlet coverage, range, backpressure correction, geometry and uncertainty |
| Electrical input | Suitable power analyzer operated under the approved electrical procedure | Hire service or rent | Actual supply/load compatibility, safe connection and calibration |
| Sound | Calibrated sound instrument with its check equipment | Hire service or rent | Method, location, background noise and calibration |
| Temperature/humidity | Logging instrument near particle sampling locations | Buy appropriate logger | Recorded locations, calibration and response time |
| Room dimensions | Tape/laser distance instrument plus room/ventilation survey | Buy/use existing | Actual usable room geometry, connected spaces and opening state |
| Data capture | Existing laptop and original instrument exports | Use existing | Clock synchronization, USB/export support and run metadata |

Two room monitors help detect spatial differences; they are not automatically an upstream/downstream filter-efficiency pair. These quantities do not constitute reference-grade particle testing or whole-device HEPA certification.

## Checked candidate: SPS30 particle monitoring

**OEM FACT:** [Sensirion SPS30 data sheet](https://sensirion.com/media/documents/8600FF88/64A3B8D6/Sensirion_PM_Sensors_Datasheet_SPS30.pdf), version 2.0–D1, June 2023, pages 2–3 and 16, retrieved 3 October 2026: mass range 0–1,000 ug/m3. PM2.5 precision below 100 ug/m3 is +/-[5 ug/m3 + 5% of measured value]; above that, +/-10%. The sheet describes this precision as device-to-device variation, not the complete uncertainty of our experiment. Supply is 4.5–5.5 V. UART/I2C are available; I2C address is 0x69. OEM cautions about cable interference and recommends UART where possible.

**RECOMMENDATION:** evaluate two matched ready-to-log instruments before buying bare modules. If SPS30 is chosen, obtain the exact bridge/board/cable documentation. Use co-location and comparison against suitable reference equipment where available. Do not infer a detection limit from the precision formula, or claim a small difference between sensors is real cleaning. The usable floor for decay analysis is still UNKNOWN.

## Checked candidate: filter-pressure monitoring

**OEM FACT:** [Sensirion SDP8xx digital data sheet](https://sensirion.com/file/datasheet_sdp800-d/), version 1.1, April 2019, pages 2–3 and 6, retrieved 3 October 2026: SDP810-500Pa uses tube connections and measures -500 to +500 Pa; I2C address 0x25. SDP811-500Pa uses 0x26. Supply is 2.7–5.5 V; media compatibility is non-condensing. Published zero-point accuracy is 0.1 Pa plus span accuracy 3% of reading under stated test conditions. These are not our installed tubing/measurement uncertainty.

**RECOMMENDATION:** keep this family as a candidate, not a selected range. Confirm maximum differential across each filter at the actual loaded/fault conditions first. Overpressure survivability is not a valid measurement range. Use a bought/rented calibrated instrument with adequate range for commissioning. Confirm sign, zero/reference check, tap placement and contamination/condensation protection without introducing an uncharacterized restriction. Do not interpret pressure directly as airflow without a calibrated relationship.

## Connection issue found before ordering

**INFERENCE from the documented addresses:** two SPS30 units share 0x69; two SDP810 units share 0x25. Identical-address units cannot be separately addressed on one unswitched I2C bus.

Review one of these arrangements before selecting cables/boards:

- Separate supported USB/UART acquisition paths for the room monitors, with short local sensor connections. Actual bridge compatibility remains UNKNOWN.
- Separate controller buses or a reviewed I2C multiplexer for duplicate addresses.
- For pressure only, the documented SDP810/SDP811 address pair is an option if both ranges and exact supplied variants are acceptable.

No pin assignments, pull-up network, power adapter, controller SKU or cable-length release is given here. An interface name alone does not establish voltage compatibility. No live acquisition driver exists yet, and none of these paths controls the mains fan or its safety functions.

## Airflow instrument reference—not a purchase recommendation

**OEM FACT:** [TSI AccuBalance 8380 specification](https://tsi.com/getmedia/b057b3f8-c6c6-425f-ac69-c62a0dfb907e/8715-8380_AccuBalance_US_5001431?ext=.pdf), page 3, reviewed 3 October 2026: capture-hood range 42–4,250 m3/h. Its published accuracy above 85 m3/h is +/-3% of reading +/-12 m3/h. This is a range reference; college possession, price and availability are UNKNOWN.

The exploratory 1,200–1,300 m3/h target lies inside that catalogue range, but this does NOT establish suitability for our outlet. Operator must assess fit, discharge pattern and instrument-induced backpressure. Alternatively obtain a reviewed traverse method with suitable straight measurement geometry. Do not use one centre-point airspeed reading times gross grille area as validated whole-device flow. The earlier short outlet study is not an approved measurement section.

## Where the instruments go

```text
Air path (not to scale):
intake -> P0 -> prefilter -> P1 -> HEPA -> P2 -> fan -> outlet flow measurement
            |                |             |
            + DP_PREF high   + DP_PREF low  + DP_HEPA low
                             + DP_HEPA high

Room PM A and room PM B: independent recorded positions outside the tower.
Temperature/humidity: recorded room position(s), not assumed sensor-chip temperature.
Power analyzer: electrical reviewer-approved measurement arrangement only.
Laptop: receives data; NO connection to fan safety functions.
```

P0/P1/P2 are conceptual static-tap locations, not drilled-hole dimensions. Choose actual positions/geometry with the test mentor to avoid local velocity effects. P1 can feed separate reference tubes to the two instruments only through reviewed airtight connections. Record positive convention as upstream minus downstream and check it before measurements. A physical tubing/installation drawing is still required.

## Exact next action without a college lab

Obtain supplier/service quotes using the equipment sheet: model, range, calibration/reference record, availability date and export method. Include competent airflow measurement and qualified mechanical/electrical review as paid scopes where needed. ENTC review is optional and does not replace assistant preparation. Do not buy a Raspberry Pi or sensors simply to fill a blank BOM row. Once instruments are confirmed, we can write the matching export/live adapter and complete the measurement installation drawing.

No request sent, equipment obtained, parts ordered or physical data collected. Existing [test gates](BUILD_AND_TEST.md), [recorder](MEASUREMENT_RECORDING.md) and [exploratory analysis](INDOOR_DECAY_ANALYSIS.md) remain the workflow. Outdoor sensing/weather protection is a separate later design.

## Source audit

Archived under `data/monitoring/sources/`; downloaded 3 October 2026. Sensirion specification table pages were rendered and visually checked. Keep OEM copyright; review redistribution permission before public publication.

| PDF | SHA256 |
|---|---|
| SPS30_review_2026-10-03.pdf | 93573ca35f7e239b947b78b31568812972dc6ca49fe558837e2efc3d37b5421a |
| SDP8xx_digital_review_2026-10-03.pdf | dbcbad9c96a414903676b160715a082126f0a5f6fe37441114965aebebbf9835 |
| TSI_8380_review_2026-10-03.pdf | f478a890a0a5ce98990d18f7902b28bbee03df591c49074619c5994cec8f04a5 |
