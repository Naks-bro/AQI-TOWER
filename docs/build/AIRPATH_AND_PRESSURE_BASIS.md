# Air path, transition and pressure accounting — M04 study

2 October 2026. PRELIMINARY. No component selection, fabrication release or new CFD.

## Physical work completed

Created three hollow CAD parts in a separate fit-study document: square-to-round transition, short inlet neck and straight circular outlet. This develops the R02 candidate layout without changing R00/R01/R02. It is not fitted to detailed OEM fan CAD.

Files: `cad/packaging/AQI_M04_Airpath_STUDY.FCStd`, `AQI_M04_Airpath_NOT_FOR_FABRICATION.step`, `M04_AIRPATH_AUDIT.json`; configuration `cad/parametric/airpath_m04_study.json`; generator `scripts/geometry/create_airpath_study.py`.

```text
          Required outlet guard: not selected or modeled
                            ↑
        Circular outlet: 315 mm clear bore ASSUMED, 200 mm long
                            ↑
                Candidate fan: not modeled here
                            ↑
        Short neck: 315 mm clear bore ASSUMED, 10 mm long
                            ↑
       Square-to-round transition: 563 mm -> 315 mm, 215 mm high
                            ↑
             Sealed clean plenum / air above HEPA
                            ↑
             Retained and sealed HEPA cassette
```

Transition base z=965 mm is 20 mm above the illustrative R02 retainer top. Its top is z=1180 mm; neck ends at z=1190 mm. Outlet starts z=2015 mm and ends z=2215 mm. These coordinates align with the bounding-envelope study, not verified actual fan inlet/outlet axes. A flange, mount or terminal enclosure may change the fit.

315 mm is an assumed **internal flow diameter**. The S&P drawing's 312 mm connection dimension is not proof of a 312 mm internal bore. Spigot wall, mating tolerances, clamp and gasket must be established by an actual connection drawing. Do not machine an adapter from these assumptions.

CAD uses 2 mm profile offsets, not uniform normal wall thickness or developed sheet-metal panels. Regenerate from the JSON for profile changes; the shapes are generated snapshots, not spreadsheet-linked parts. FreeCAD checks found three valid solids; native file reopened and STEP reimported with three valid solids. No structural, service, leakage or installed aerodynamic validation was performed.

## Why we are not adding a narrow jet nozzle yet

A simple same-bore outlet is the first comparison baseline. A smaller nozzle raises discharge velocity and can increase required fan pressure and noise. Entrainment mixes surrounding air but does not mean that air has passed through the filter. We can compare outlet shapes later; there is no evidence yet for a Dyson-like outdoor bubble.

At assumed 1,300 m3/h and density 1.2 kg/m3, a 315 mm clear duct has mean velocity 4.63 m/s and velocity pressure 12.88 Pa. These are arithmetic screening values, not measured fan velocities.

## Pressure basis: what must be matched

[AMCA's fan-curve explanation](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/straightening-out-fan-curves.html) distinguishes fan total pressure, static pressure and outlet velocity pressure. Use the manufacturer's actual stated area and test definition, not an arbitrary casing dimension.

For the simplified ambient-intake to free-discharge system considered here, with uniform flow and no external static backpressure:

```text
Fan total-pressure requirement
    = sum of internal irreversible losses + terminal velocity pressure

Fan static-pressure requirement
    = fan total-pressure requirement - fan outlet velocity pressure

Therefore:
    static duty = internal losses + terminal VP - fan outlet VP
```

When the fan outlet and final discharge have the same effective flow area, their velocity-pressure terms cancel. In that special case the fan static duty is the internal irreversible loss sum. Adding the free-jet velocity pressure again to that sum while using the static fan curve would double-count it. Guard/duct/transition losses still remain.

If the outlet area changes, keep both terms and include the new fitting's loss. Static pressure difference measured between fan taps is not automatically AMCA fan static pressure; inlet velocity and measurement planes matter. Nonuniform flow, external pressure, swirl and installed fan effects require additional analysis. We have not verified the actual OEM flow area or test-installation match, so this does not certify a selection.

Earlier 50/100 Pa hardware inputs are broad sensitivity assumptions, not reconciled measured system-static resistance. Prior fan intersections remain illustrative. This clarification does not silently turn them into confirmed performance.

## Component-by-component loss sensitivity

Run `python scripts/analysis/airpath_loss_screen.py`. It uses an assumed 70% intake free area, 315 mm clear round duct, and explicitly ASSUMED coefficients/friction factors. The numerical endpoints are study inputs, **not evidence-based design bounds**.

| Component | Low-input scenario Pa | High-input scenario Pa |
|---|---:|---:|
| Combined intake entry + guard | 14.92 | 39.78 |
| Square-to-round transition | 1.29 | 6.44 |
| Outlet guard | 12.88 | 38.65 |
| Connections/joints | 1.29 | 6.44 |
| Equivalent fan installation effect | 0 | 25.77 |
| 210 mm modeled straight round length | 0.16 | 0.30 |
| Total hardware sensitivity | 30.53 | 117.38 |

The transition coefficient is referenced to round-throat velocity; intake coefficient to assumed guard-passage velocity. These coefficients were NOT obtained from an OEM fitting curve. The calculation exposes which data we need; it does not validate a smooth-looking CAD loft. Values outside this range are possible.

With same-area fan/terminal cancellation, adding the previous illustrative filter assumptions gives:

- Clean filter scenario: approximately 163–250 Pa required static duty at 1,300 m3/h.
- HEPA 2x resistance plus prefilter 80 Pa-at-reference scenario: approximately 326–413 Pa at the same flow.

These are not new fan operating points or approved dirty-filter thresholds. A larger intake/low-loss guard can help; it does not remove the HEPA resistance. Rain louvres, silencers, bends and optional carbon are absent; add their losses if introduced.

## Installation-effect issue still unresolved

The inlet neck is only 0.032 duct diameters long, and the outlet is 0.635 diameters. [AMCA's system-effect guidance](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/mitigating-system-effect-to-optimize-fan-performance-efficiency.html) discusses nonuniform outlet flow and an illustrative 2.5-diameter outlet-length rule of thumb under its stated conditions. It is not a universal requirement for this particular mixed-flow fan.

Do not assume a compact 200 mm outlet reproduces catalogue performance. Ask the selected OEM to accept the inlet contraction, straight lengths, guards and outlet arrangement, or provide correction/installed testing. Simply adding long ducting may make the tower impractically tall; another fan architecture or layout could be preferable. [DOE's fan guidance](https://betterbuildingssolutioncenter.energy.gov/better-plants/fans) also emphasizes managing inlet/outlet flow uniformity.

## Required decisions before the next mechanical release

1. Fix minimum useful flow from the actual indoor test-room volume and a mentor-approved demonstration target; define the outdoor pilot setting separately.
2. Obtain selected fan flow area, installation geometry, numeric curve and inlet/outlet guidance. Do not select a fan only because it fits the cylinder.
3. Select commercial or engineer-reviewed guards with documented free area, loss and access protection; hole size alone does not establish safety.
4. Replace coefficient guesses with supplier data, defensible correlations or controlled measurements. Reconcile pressure basis at named planes.
5. Integrate adapters, supports, flanges and service access into the assembly. Confirm sheet-metal manufacturability and approved seals.

Final fan choice, exact wiring, protection ratings and fabrication sheets remain unreleased. The next useful input is actual room dimensions and the intended outdoor location type, rather than another assumed coverage circle.
