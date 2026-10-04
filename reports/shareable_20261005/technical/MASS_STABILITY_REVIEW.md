# R03M mass and stability supplement — 5 October 2026

**NOT RELEASED. Physical prototypes: 0. No complete-device weight or stability rating.**

## What changed

- DETECTED: nominal CAD foot-contact hull is [(25.0, 15.0), (525.0, 15.0), (525.0, 345.0), (25.0, 345.0)] mm in CAD x/y. This assumes all four feet contact a flat floor without deformation.
- DETECTED: the DXF has 2822 holes per face. Subtracting these from the solid CAD guard proxies removes 0.557 kg at assumed steel density7850 kg/m3. Native CAD remains unchanged and solid-faced.
- VERIFIED OEM SPECIFICATION: ARCTIC P14 Max ACFAN00287A net weight245 g each, four fans0.980 kg. Actual mass location is UNKNOWN; this screen uses the CAD geometric centroid as an ASSUMPTION. Source: [ARCTIC specification sheet](https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf), accessed5 October2026.
- ASSUMED: panel650, cleat600 and metal7850 kg/m3. These are not confirmed material grades or delivered component weights.
- RESULT: corrected partial modeled mass plus specified fan mass is **12.613 kg**; partial centroid **(275.04, 180.11, 365.55) mm**. This is not a whole-device estimate or guaranteed lower bound.
- UNKNOWN: 29 modeled objects still lack usable mass information, including filters, feet, seals and control/cable reservations. Unmodeled finishes, real wiring and fabrication variation are also excluded.

## Useful warning, not a pass

For this partial assumed assembly ONLY, outward horizontal force at631 mm above the nominal floor gives a weakest-edge static tipping balance of **32.3 N**. The partial geometry's weakest downslope tipping angle is **24.3 degrees**. Do not use either number as a finished-device limit: the actual mass distribution is not established. Sliding may happen first; friction is unknown. This is not a prescribed safety test load.

RECOMMENDATION: keep the first demonstrator indoors on a controlled flat floor, isolated from casual pushing and cable trip hazards. Do not call it suitable for public/outdoor installation. Anti-tip attachment or a broader support concept requires an assessed substrate, fixing loads and structural design, not an arbitrary ballast choice.

The same OEM sheet specifies0–40 C operating ambient. This is a limitation for eventual hot outdoor use; it does not establish weather sealing, solar-heated enclosure temperature or vandal resistance.

## Reproduce and close the gap

Run `python scripts/analysis/d01_mass_stability.py` and `python scripts/analysis/test_d01_mass_stability.py` from repository or packaged engineering root. JSON contains exact input hashes, signed hole-removal mass rows and each directional edge result. Historical `mechanical_screen.json` is preserved; its solid-face subtotal is superseded only for this corrected partial mass calculation.

To calculate a real full-device CG: record net installed mass and mass location for every omitted item, confirm selected material density/finished dimensions, include wiring/finishes and service configurations, and weigh the assembled device. Then assess joints, actual foot contact/friction, push/cable loads, floor/incline and filter-removal scenarios with qualified mechanical review. No build release is granted by these arithmetic checks.
