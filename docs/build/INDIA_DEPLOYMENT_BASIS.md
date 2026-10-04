# India deployment basis — heat, public access and size

3 October 2026. Applies to D01 and the eventual outdoor tower. **Engineering recommendations, not construction release.** User has explicitly requested Indian temperature suitability, robustness against public misuse, size and location to be considered. Physical prototypes: 0.

## Decision in plain language

**D01 is an indoor learning prototype, not an outdoor street product.** Retain its assembly to test real fan/filter performance and sealing. Do not place it outdoors or leave it accessible to the public. Putting a metal cover around it would not qualify its fans, filters, controls or structure for heat, rain or tampering.

Recommended first host: a supervised room in a college or NGO building, with an identified operator, safe power and permission to test. No lab is assumed. After a separately qualified outdoor assembly exists, the first outdoor pilot should be an operator-managed campus/NGO courtyard or sheltered waiting area with staff oversight, maintenance access and approved anchoring. A shelter does not remove wind-driven rain or public-access requirements. Do not start at an unattended roadside, traffic island, exposed bus stop or flood-prone location.

Intended eventual application: investigate local particle reduction near a defined occupied waiting/seating area. This is not a city-wide pollution solution or a proven clean-air bubble. Record wind and background pollution and compare conditions at occupied locations; do not infer radius/spacing from fan flow. Avoid claims of gas removal or protection from vehicle exhaust as a whole.

## Heat: present component fails the blanket outdoor assumption

**VERIFIED OEM FACT:** ARCTIC lists P14 Max operating ambient as 0–40 C. **VERIFIED CLIMATE EVIDENCE:** IMD's Telangana extremes table updated to May2025 lists Hyderabad at45.5 C. This is an observed extreme, not a complete design climate or a limit for all India. Even without solar heating it exceeds the fan limit by5.5 C. Actual conditions for Pune/Mumbai and the chosen site remain to be established.

**RECOMMENDATION for D01 tests:** dry indoor operation, no direct sunlight; use35 C at the fan inlet as a provisional screening ceiling, leaving5 C to this fan's maximum. Measure fan-inlet and supply/controller enclosure temperatures at full load and during reduced-airflow conditions using an agreed safe procedure. Follow the lowest actual component rating. This is NOT an implemented cutoff or permission to energize: supply/controller thermal limits, startup and existing restart-protection gates remain open. Do not operate deliberately outside OEM limits.

**OUTDOOR DESIGN REQUIREMENT:** set site ambient, solar exposure, enclosure temperature rise, humidity/condensation and storage limits before final component selection. As an initial hot-site sourcing screen only, investigate components for50 C external ambient plus the verified local enclosure rise; a hypothetical10 C rise would require suitability at60 C at the component. Neither number is an approved India-wide design condition. Temperature-rated industrial fans may be needed. A light-coloured shaded shell and ventilated air path are candidate measures, not proof of adequate cooling. Do not seal electronics into an unverified hot box.

## What the public version needs

| Exposure | Design direction to carry into the assembly | Evidence needed before public deployment |
|---|---|---|
| Rain, wet cleaning and flooding | Downward-facing/weather-baffled openings, separated drainage, raised dry electrical compartment; no water route to filter or electrics | Installed ingress assessment/test, chosen site flood/drainage review; no IP claim yet |
| Dust and insects | Accessible replaceable screen/prefilter only after pressure budget supports it; sealed filter edges; no uncharacterized restrictive mesh | Supplier pressure curves, loading checks and maintenance interval from actual conditions |
| Kicking, leaning and thrown objects | Load-bearing metal frame, replaceable tough panels, protected filter faces, recessed controls and rounded edges | Selected grade/thickness, joints, deformation and reach checks; impact test plan for applicable classification |
| Theft and opening panels | Lockable service door, captive/tamper-resistant fasteners, concealed anchors and cables, no exposed removable filter or fan fixings | Access/retention review and service procedure; tamper-resistant is not vandal-proof |
| Tipping and climbing | Engineered anchoring to an approved substrate; no easy footholds; not a seat/table; avoid movable castors in public use | Full mass/CG, support geometry, wind/misuse loads, substrate and anchor verification |
| Corrosion, sunlight and humid/coastal exposure | Site-appropriate coated metal or corrosion-resistant alloy; protected cut edges, compatible fasteners and UV-suitable exterior materials | Actual coating/material specification, joint compatibility and exposure tests; material not selected yet |
| Fans, sharp edges and electrics | Independently retained guards, protected wiring, tool-controlled service access and deliberate restart after interruption | Mechanical reach/deflection and qualified electrical/commissioning review; no Arduino-only safety function |

IP refers to ingress protection and IK to mechanical-impact classification. They are different. A rated purchased box does not rate the whole tower after holes, glands, vents and doors are added. Use IEC60529 and IEC62262 as classification references while the reviewer establishes the applicable product standards and Indian requirements. No IP/IK certification or exact target rating is claimed here. Do not perform improvised impact/water tests on energized equipment.

The current plywood panels, exposed filter faces, projecting studs, external control reservation and shared guard bolts are **not public-product details**. A public version needs engineered replacements, not just paint or cosmetic sheet wrapping. Guards must remain secure during ordinary access; the current shared-bolt arrangement does not establish that.

## Size and airflow consequences — actual calculations

**DETECTED design envelope:** D01 is roughly590 W x490 D x631 H mm including the current control/stud reservations, not merely its550 x360 cabinet. It is a floor-sized demonstrator, not a pocket-size model. Service clearances and protected cables add to occupied space; these are not included in the envelope.

A circular sleeve enclosing that rectangular envelope requires about767 mm internal diameter before clearance; with an **assumed**25 mm radial allowance it is about817 mm ID. This is a conservative rectangle-fit screen, not a selected cylinder dimension. No wall, hood, airflow/service clearance or weather protection is included. Therefore do not promise a slender Dyson-like cylinder by wrapping D01: a slender version would need different internal packaging and possibly different filters. Keep R01 unchanged until real parts establish the next packaging decision. Final outdoor height/diameter remain UNKNOWN.

The new script also adds illustrative weather/guard loss of0/5/10/20 Pa at300 m3/h to the existing middle-filter scenario. Loss scales with flow squared; these are **not measured hood coefficients**. Read `reports/prototype_d01/component_validation/deployment_screen.json` for the solved operating points. This demonstrates why rain baffles, anti-vandal screens and extra filters cannot be added without recalculating fan duty.

For stability, illustrative10/20/30 kg units with assumed150 mm CG-to-support-edge distance and a push at631 mm height would start static overturning at approximately23/47/70 N. These are NOT actual D01 capacities, rated test loads or acceptable thresholds. Real mass/CG, support polygon, sliding, dynamic impact and anchors are unknown. The calculation shows why adding weight or a wide cosmetic shell is not a substitute for proper anchoring.

## Fast route, without restarting the project

1. Keep building toward the existing D01 indoor particle test. Exact filter resistance/dimensions, guards/joints/seals and restart protection still need closure; no decorative cylinder is on the critical path.
2. Use measured airflow, leakage, temperature and power to select the outdoor fan/filter core. Do not scale from partial historical CFD or unmeasured D01 predictions.
3. Apply the public-use requirements above to one integrated outdoor assembly. Choose its site before freezing anchors, weather design, noise and pedestrian/service clearances. A named host/operator and maintenance responsibility are prerequisites.

Next external decision eventually needed: **the actual host location and indoor test room**, not necessarily a city today. College/NGO funding does not imply site approval or maintenance staffing. No purchase, installation, supplier contact or public deployment is authorized by this document.

## Sources and reproducibility

Accessed2026-10-03:

- [ARCTIC P14 Max black product page](https://www.arctic.de/en/P14-Max-Black/ACFAN00287A) — operating ambient0–40 C. Existing archived specification PDF corroborates the thermal limit; earlier SKU/curve discrepancies remain documented separately.
- [IMD Telangana extremes, updated May2025](https://mausam.imd.gov.in/hyderabad/mcdata/tlngextwx.pdf) — Hyderabad45.5 C. Not a site design-weather study.
- [IEC60529 official scope](https://webstore.iec.ch/en/publication/2447) — ingress classification.
- [IEC62262 consolidated official scope](https://webstore.iec.ch/en/publication/71109) — external mechanical-impact classification. Public scopes reviewed; no purchased standard or claim of full compliance.

Run `scripts/analysis/d01_deployment_screen.py` using existing Python. Five arithmetic/regression checks; no new simulation, physical result or material strength certification. The aqi-build-review skill required the indoor/outdoor boundary and added-loss consequences to be explicit. Historical models remain unchanged.
