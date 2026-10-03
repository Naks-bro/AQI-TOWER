# Cylindrical tower: Dyson inspiration and outdoor lessons

2 October 2026. User-requested design alternative. PRELIMINARY comparison; no concept frozen, no fabrication CAD generated.

## What we can learn from HushJet

[Dyson's official HushJet page](https://www.dyson.com/air-treatment/air-purifiers/hushjet) describes 360-degree filters and a shaped high-velocity discharge that entrains surrounding air. It describes passive electrostatic particle media, not a powered ionizer. These are manufacturer descriptions of its indoor product, not measured results for our project.

Useful principles: intake distributed around a body, accessible replaceable cartridges, sealed clean/dirty compartments, and careful outlet/noise design. Do not copy the proprietary nozzle geometry or assume scaling its appearance produces the same performance. Entrained room air increases mixed jet flow, not filtered clean-air delivery. A narrower nozzle can raise pressure loss and noise; it is not free additional purification.

## Three practical options

| Option | What it looks like | Build advantage | Main drawback |
|---|---|---|---|
| A: cylindrical outer shell, standard panel-filter core | Rounded metal exterior around replaceable rectangular cassette | Standard documented filters; quickest service/procurement route | May be wide; circular appearance does not establish true radial filtration |
| B: polygonal bank of panel filters | Multiple flat cassettes around central clean plenum and fan | Radial intake using standard panels; more filter area | More seals, cassettes and loaded-flow balancing; airflow/structure redesigned |
| C: genuine cylindrical cartridge | Radial flow through ring-shaped filter into central core | Compact coherent circular architecture | Need suitable documented cartridge curves, leak-tight end seals and dependable replacement supply |

RECOMMENDATION: compare A and C first; keep B if standard panel suppliers offer a convincing low-loss arrangement. Do not select C just because it looks most like Dyson. Do not stretch the previous GEO_C model into a cylinder and reuse its results.

If a 593 x 593 mm square filter is placed across a circular cross-section, its diagonal alone is about 839 mm. The shell must be larger after clearance, frame and wall allowances. That geometric constraint applies only to this orientation; an upright cassette layout must be checked separately in the assembly. A small cosmetic cylinder will not contain the present candidate automatically.

For a radial cylindrical cartridge, gross cylindrical area is pi x diameter x active height. Example assumptions D=0.6 m, H=0.6 m give 1.13 m2 and about 0.32 m/s gross radial face velocity at 1,300 m3/h. This is a sizing illustration, not a filter selection: pleated media area, core restrictions, end caps and supplier pressure curves determine real behaviour.

Conceptual air route (not an approved arrangement):

```text
               guarded outlet
                     ^
              reviewed fan module
                     ^
               clean central path
                     ^
 intake around body -> coarse filter -> sealed particle filter
              base + isolated electrical compartment
```

For the outdoor version, outlet direction/height is an open design question. A jet upwards may mix or escape rather than benefit breathing height; low outlets can recirculate or create public-access hazards. Compare configurations using site wind and breathing-height measurements, not marketing resemblance.

## Government projects: what was established

[PIB's 29 July 2024 statement](https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2038298&lang=2&reg=48) lists government-supported trials including NEERI traffic-junction purification units, bus-roof filtration and an IIT Bombay/Tata Projects smog tower. The tower involved substantial infrastructure and operating costs; the announcement is not proof that any outdoor purifier succeeds.

The [Delhi Economic Survey 2025–26](https://delhiplanning.delhi.gov.in/sites/default/files/2026-03/economic_survey_english_0.pdf), printed page 127 (PDF page 140), says the Connaught Place pilot became operational in September 2021, was assessed by IIT Bombay, and had limited effectiveness because the filtered-air jet's influence was too small. Its narrative and tabulated distance summaries differ; do not extract a guaranteed 500 m radius from it. No numerical tower efficiency is transferred to our design.

Our inference: copying the scale or appearance of a government tower is not sufficient. Keep the first outdoor objective local and testable: useful reduction at defined occupied points, under recorded wind, for reasonable energy and maintenance. Source control remains important. A chain is a hypothesis to test after one unit demonstrates benefit.

## Real component families to investigate — NOT an order list

| Function | Public OEM candidate/source | What still has to be obtained |
|---|---|---|
| Circular duct fan | [Systemair K AC/EC family](https://www.systemair.com/en/products/fans/duct-fans/circular-duct-fans/k), [India catalogue/contact](https://www.systemair.com/en-in/products) | Exact India SKU, duty curve with loaded filters, envelope, acoustics, control diagram and quote |
| Centrifugal EC blower | [ebm-papst air-purifier fan portfolio](https://www.ebmpapst.com/gb/en/industries/ventilation/air-purifiers.html) | Select exact RadiCal/other model at duty point; inlet/mounting design and protection requirements |
| Particle filter | Existing Freudenberg panel candidate as reference; request documented panel alternatives or cylindrical cartridge from qualified suppliers | Actual dimensions, multi-point clean/loaded curves, unit certificate, sealing and replacement availability; no suitable cylindrical HEPA SKU confirmed yet |
| Optional gas cylinder | [Camfil CamCarb family](https://www.camfil.com/en/products/molecular-filters/cylinders) | Gas-specific media and breakthrough/pressure data; these are molecular/carbon filters, NOT HEPA particle cartridges |
| Housing | Local folded/rolled metal fabricator | Assembly drawings, material/coating, structure and weather protection |

Do not buy Dyson domestic replacement cartridges for a much larger tower without documented compatibility, pressure curves and replacement strategy. Product-family existence does not establish local stock, price or suitability. No supplier contacted and no component ordered.

## Supplier data request to finish selection

Send only after team authorization: intended particulate-only prototype, indoor commissioning/outdoor future use, provisional screening flow 1,200–1,300 m3/h (not yet accepted target), and request quotes plus dimensional drawings. Ask for fan curves including efficiency/power/noise at the proposed complete-system duty, supported speed control and safety instructions; filter initial/terminal resistance curves, certification, dimensions, mass, end-seal/gasket details and replacement lead time. Ask vendors to propose alternatives if the selected fan cannot meet loaded resistance.

The final design must choose shape AND serviceable components together. Complete architecture choice before the manufacturing drawing release, not after purchasing incompatible parts.
