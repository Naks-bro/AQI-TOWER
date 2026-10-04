# Fan selection brief R00 — ready for quotation review, not ordering

3 October 2026. Prepared by the assistant. NOT SENT. No selected fan or approved performance requirement.

## The decision in plain language

A fan must push air through the filters, not just move air in an empty duct. As filters collect dust, airflow falls unless the fan has enough pressure capability. Buying on the largest free-air number can leave us with a tower that looks complete but delivers too little filtered air.

**RECOMMENDATION:** obtain a documented higher-pressure fan proposal and a matching lower-loss alternative. Compare the complete guarded, sealed fan/filter core before committing to either. Do not force a particular fan into the cylindrical shell; adapt packaging after selection. No outdoor coverage radius is specified by this brief.

## What we know and what we do not

- FACT / user direction: indoor first trial, outdoor final goal; funded commercial review/fabrication/testing, no college lab assumed.
- DETECTED: the historical KVO model identity remains ambiguous; the S&P TD-2000/315 SILENT ECOWATT is an unselected comparison candidate with an archived OEM catalogue and visually digitized curve.
- ASSUMPTION: the study flow is 1,200–1,300 m3/h. The 1,400 point below is a comparison extension, not a raised requirement. Air density is 1.2 kg/m3.
- ASSUMPTION: filter pressure scales linearly from historical partial CFD; hardware losses follow the existing M04 coefficient scenarios. These are not measured bounds or supplier-approved dirty-filter limits.
- UNKNOWN: actual room volume, accepted minimum flow/noise, exact filter curves and terminal resistance, installed fan effects, exact purchasable fan, current prices and lead times.

## Calculated comparison at the same airflow

The table uses [M04 pressure accounting](AIRPATH_AND_PRESSURE_BASIS.md): ambient intake/free discharge, equal effective fan-outlet and terminal areas, so the terminal velocity term cancels in the static-duty comparison. Actual areas and OEM test installation remain unverified. Low/high columns are two input scenarios, NOT uncertainty limits. Coefficients outside them are possible.

| Study flow m3/h | Clean static-duty scenarios Pa | Loaded static-duty scenarios Pa | Historical KVO chart Pa | S&P digitized chart Pa |
|---:|---:|---:|---:|---:|
| 1,200 | 149–223 | 298–372 | 205 | 290 |
| 1,300 | 163–250 | 326–413 | 137 | 230 |
| 1,400 | 179–279 | 353–454 | 69 | 175 |

Clean assumption: HEPA 111.2 Pa plus prefilter 25 Pa at 1,332 m3/h. Loaded assumption: twice that HEPA resistance plus prefilter 80 Pa at the same reference flow. These are sensitivity inputs, not maintenance settings. No carbon, rain louvre, silencer, bend or narrow jet nozzle is included. Add any such parts before selection.

At 1,300 m3/h the S&P estimate is about 96–183 Pa below the loaded scenarios. Its +/-25 Pa chart-reading sensitivity is not total uncertainty. The historical KVO estimate is about 189–276 Pa below them. Neither is confirmed adequate for this assumed loaded duty. This does not prove either fan is unusable at another accepted flow or in a redesigned lower-resistance system.

A clean-case pass is not a loaded-case pass. Increasing speed without an OEM curve/limit is not an approved remedy. Final comparison needs curves at actual speeds, current/power, stable operation, sound and installation acceptance.

## Copyable supplier request — prepared, not sent

We are developing a particulate-only air-cleaning tower for a first indoor trial, using a coarse prefilter and sealed HEPA cassette. Final outdoor development is separate. Please propose exact India-supported fan/controller packages for comparison; this is a quotation and engineering-information request, not an order.

Our provisional main study flow is 1,300 m3/h. Under explicitly unmeasured assumptions, static duty is approximately 163–250 Pa clean and 326–413 Pa loaded. Please report a selection at **1,300 m3/h / 250 Pa** and **1,300 m3/h / 420 Pa**, with the latter only a rounded screening benchmark, not an approved requirement or safety margin. Include the same unit's speed settings/power/sound at both points, or explain why different units/layouts are needed. Also show coverage near 1,200 m3/h / 375 Pa. We will replace these assumptions with selected-filter/installation data before procurement.

Please provide:

1. Exact fan article/revision, motor type, compatible controller/accessories and matching numeric speed-dependent curves. State static versus total pressure, density, test arrangement and stable operating region. Do not send only free-air flow or motor watts.
2. Electrical input/current at each requested point, permitted maximums, inrush/leakage data as applicable, supply requirements, wiring manual, motor-protection reset and disconnected-speed-command behavior. Restart prevention is a project requirement; do not assume internal auto-reset is acceptable.
3. Dimensioned drawing/STEP, true inlet/outlet flow areas, spigot tolerances, mounting holes, mass, allowed orientation, cable-box/access clearances and approved vibration isolation.
4. Acceptance or correction for our compact square-to-round inlet, short neck, guards and short outlet. Current layout is an unapproved fit study. Advise a less compact arrangement if needed; identify every extra adapter/guard/accessory and loss included in your selection.
5. Sound data with method and operating point, including inlet/outlet/casing contributions where available. Catalogue sound pressure under different room/distance conditions is not a promised assembled-tower result.
6. Itemized India quote including controller, mounts, adapters, tax/freight, warranty, lead time, service and replacement availability. All currently UNKNOWN.

Please return source/manual revision and selection report. No substitute article should inherit another model's curve or wiring. We will obtain qualified mechanical/electrical review and inspect/test the actual assembled unit before use.

## How a response is evaluated

Use the [response sheet](FAN_SUPPLIER_RESPONSE_R00.csv). Missing evidence stays UNKNOWN, not PASS. Do not average critical failures into an overall score.

1. Confirm accepted flow and OEM filter maintenance conditions with the project team/reviewer.
2. Rebuild the complete clean/loaded loss budget on the supplier's pressure basis; avoid double-counted exit energy. Recalculate for their actual areas and installation.
3. Check both operation points and the intervening operating range, OEM limits and installed effects. Keep power and sound separate from airflow evidence.
4. Check exact drawing, orientation, service access, support loads and electrical/control compatibility.
5. Compare delivered cost and recurring parts/service only after technical suitability; no prices fabricated here.
6. Record a justified selection with reviewer scope, then update CAD/BOM and rated electrical E01–E06. Current sheet closes no build gate.

Possible decision outcomes: SELECTABLE_AFTER_REVIEW, REVISE_LAYOUT_OR_DUTY, INCOMPLETE_EVIDENCE, or REJECT_FOR_THIS_DUTY. None is assigned to an actual supplier response yet.

## Reproduce the table without changing prior results

From the project root:

```powershell
python -c "import sys; sys.path.insert(0,'scripts/analysis'); from airpath_loss_screen import screen; from fan_duty_screen import FANS,interp; print([(q,screen(q)['same_area_terminal_vs_fan_outlet_static_duty_clean_Pa'],screen(q)['same_area_terminal_vs_fan_outlet_static_duty_loaded_Pa'],{n:round(interp(c,q),2) for n,c in FANS.items()}) for q in (1200,1300,1400)])"
python -m unittest discover -s scripts/analysis -p 'fan_duty_screen.py'
python -m unittest discover -s scripts/analysis -p 'airpath_loss_screen.py'
```

Ten existing arithmetic/screening tests passed on 3 October 2026. No new CFD, physical measurements, power prediction or purchase selection follows from those tests.

## Sources and evidence

- [AMCA fan-curve explanation](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/straightening-out-fan-curves.html), checked 3 October 2026: duty comparison must match pressure basis, test arrangement and operating point. It does not certify this tower.
- [Official S&P catalogue](https://statics.solerpalau.com/media/import/documentation/EN_TD-SILENT-ECOWATT.pdf), archived/reviewed 2 October; new web fetch failed on 3 October. Local source/hash and chart-reading limitations remain in `data/fans/sp_td2000_315_silent_ecowatt_screening.json`. Current stock/revision not verified.
- Local calculations: `scripts/analysis/airpath_loss_screen.py`, `scripts/analysis/fan_duty_screen.py`; previous [fan decision](FAN_DUTY_DECISION.md). Historical HEPA input is digital, partial/nonconverged evidence, not a physical new-cassette curve.

Next useful external input is one complete OEM selection response plus filter pressure curves—not another guessed fan envelope. No supplier has been contacted through this brief.
