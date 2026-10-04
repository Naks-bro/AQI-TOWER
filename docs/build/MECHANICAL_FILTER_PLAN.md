# Mechanical and filter plan

PRELIMINARY — NOT FOR FABRICATION. 2 October 2026.

Delivery basis updated 3 October 2026: assistant prepares mechanical CAD/calculations; use scoped paid mechanical review and local fabrication, not assumed college facilities. See [no-lab route](NO_LAB_BUILD_ROUTE.md). A fabricator's ability to make a part is not by itself structural approval.

## Design basis

Current deployment requirements: [India deployment basis](INDIA_DEPLOYMENT_BASIS.md) records user-requested heat, rain, misuse, anchoring, footprint and service-site constraints. These apply to the eventual public assembly; D01 is an indoor demonstrator only. Adding protective screens/weather baffles changes fan duty and must be recalculated.

Use the existing 2,000 x 800 x 700 mm tower envelope only as a packaging starting point. It is not an approved outer size. Candidate prefilter: 592 x 592 x 48 mm; candidate HEPA: 593 x 593 x 292 mm. Exact tolerances, frame orientation, gasket location, mass and installation clearance must come from the supplied units' drawings.

Do not put the 292 mm filter into a 30 mm simulated slot. Make an assembly with physical solids first; then extract the revised air volume and rerun airflow checks. The old CFD result does not transfer automatically.

## Physical modules

| Module | Preliminary design | Required detail before manufacture |
|---|---|---|
| Base and frame | Metal support frame; stable floor mounting | Complete mass, centre of gravity, weld/bolt sizing, anti-tip strategy, floor anchoring permission |
| Intake | Guarded, large-area opening with replaceable coarse filter | Open area, guard pressure loss, finger access assessment, no sharp edges |
| Prefilter | Separate slide-in cassette; washable only if OEM permits | Supplier clean/loaded curve, removal direction, gasket and drying/replacement procedure |
| HEPA cassette | Positive stops and controlled perimeter gasket compression | OEM gasket compression, flatness, tolerances, clamping and installed leak test |
| Clean plenum | All air must pass HEPA before reaching fan | Airtight panel seams; seal the simulated bypass path physically |
| Fan module | OEM mounting on independent metal support and vibration isolation | 20 kg historical fan mass is not suitable for thin panel or printed bracket support |
| Outlet | Guarded discharge with smooth transition | Noise, recirculation, pressure loss and indoor draught assessment |
| Electrical compartment | Separate accessible enclosure outside dirty air path | Cable glands, bonding, heat removal and moisture protection |
| Service doors | Retained fasteners/latches and gasket | Access to filters without exposed live conductors or reachable spinning fan |
| Future carbon bay | Removable blank/sealed module in first build | Physical volume and pressure budget; no loose biochar powder near fan/HEPA |

## Filters and useful pressure measurements

Provide static pressure taps before/after each fitted filter and around the fan where installation permits. Label tubes and keep fittings airtight. Instruments must cover expected dirty-filter pressure and survive overpressure; sensor range is not selected just from a clean result.

The HEPA element's class does not certify the assembled tower. Bypass through frame gaps or doors can defeat good filter media. Obtain element documentation; have the installed assembly leak-tested by a suitable service if claiming HEPA-level performance. Ordinary PM sensors cannot establish 99.95% whole-device efficiency.

Replacement limit: whichever happens first—OEM terminal pressure limit, measured flow falling below the accepted minimum, visible damage, failed seal/leak test, or unsafe operation. A provisional prefilter 80 Pa value in the previous phase is not an approved maintenance specification.

## Manufacturing approach

RECOMMENDATION: outsource a metal frame and folded sheet enclosure locally; buy standard fan, filters, certified power components and duct adapters. Sheet thickness, metal grade, corrosion coating, bolts, wheels and mounts are UNKNOWN until loads and supplier processes are reviewed.

3D print only low-risk items such as sensor brackets, label holders and fit-check templates. Do not use unreviewed printed parts for fan support, mains enclosure, high-temperature components, structural anchors or the sole HEPA seal. Printed porous adapters may leak; validate any used in the air path.

Outdoor version additionally needs rain ingress strategy that does not wet HEPA, weatherproof electrical compartment, drainage separated from treatment, corrosion control, wind load/anchoring, public-access guards, vandal resistance and service access. IP44 fan data does not confer IP44 on the complete tower. Indoor unit is not approved for rain.

## Calculations and drawings still required

First mass/load-path screening now exists in [M02 weight and stability review](M02_WEIGHT_STABILITY.md). Nine CAD study shapes give 135.6 kg using assumed steel density; this excludes actual fan/filters/frame/base/electrics. Full mass/CG, member/joint sizing and actual tipping/sliding review are still required. No material or thickness is approved.

- Drawing M01: general assembly with true component solids and access envelopes.
- M02: frame/base, mass and centre-of-gravity sheet, lift points and fastener schedule.
- M03: filter cassette section with gasket/clamp tolerances and bypass closure.
- M04: fan mounting, adapters, vibration isolation and guards.
- M05: service doors and separate electrical compartment.
- M06: sheet-metal cut/fold drawings and assembly sequence; printable parts separately marked.
- Calculate velocity from effective open area (not gross panel area), complete pressure losses at clean/loaded conditions, fan operating points and uncertainty.
- Stability screening: restoring moment = total weight x horizontal distance to tipping edge; compare with lateral load x its height and other overturning loads using engineer-approved factors. Outdoor wind uses site gust design criteria, not the 1 m/s airflow illustration.

Release requires suitably qualified mechanical review, fabricator manufacturability/inspection acceptance, fit review against actual supplier drawings, and updated simulation or justified analytical checks of the new air path. No college reviewer is assumed available.
