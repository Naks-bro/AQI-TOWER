# M05 real hardware and gasket check

2 October 2026. PRELIMINARY — NOT FOR FABRICATION OR PURCHASE.

## Plain-language outcome

The previous hatch model reserved space for eight small blocks, not real locks. Actual latch drawings do not fit those reservations unchanged. Squeezing a gasket can also require much more force than air pressure puts on the door. We must design the closure around real parts, not order eight latches from the sketch.

## Manufacturer evidence

Two reference families from [Southco's C5 drawing](https://files.southco.com/static/Literature/c5.en.pdf), printed pages 136–137, reviewed 2 October 2026:

| Reference, not selected SKU | Body, mm | Panel cutout, mm | Published maximum static load |
|---|---|---|---|
| C5 90 mm | 110 x 50 | 90 +/-1 x 35 +/-1 | 445 N |
| C5 71 mm | 80.5 x 35.5 | 71 +/-1 x 25 +/-1 | 290 N for grip 1–25 mm; 170 N for 15–30 mm |

The larger lever drawing shows up to 85 mm projection when raised; the smaller shows a 50-degree open position. Complete motion/catch clearance is not checked. Static-load figures are NOT validated gasket-closing forces. Neither supplier nor exact SKU is selected. Availability, price and lead time are UNKNOWN.

**DETECTED calculation:** even the smaller cutout's minimum width, 24 mm, exceeds our assumed 15 mm flange land. Neither cutout fits wholly within that rim. This does NOT prove either latch cannot be mounted elsewhere through the cover: repositioning requires a new catch/support/seal and operating-clearance design. Do not cut holes from the present study.

## Why the 3 mm gasket space is not a specification

Example only: [Rogers PORON 4701-40 data sheet](https://www.rogerscorp.com/-/media/project/rogerscorp/documents/elastomeric-material-solutions/poron/english/data-sheets/17-007-poron-4701-40-soft.pdf), publication 17-007 / 0724-PDF, page 1, reviewed 2 October 2026. The 240 kg/m3 grade lists 27–76 kPa compression stress at 25% deflection, test speed 0.51 cm/min; typical 41 kPa. Nominal thickness range starts at 3.18 mm with +/-10% thickness tolerance. This is reference material data, not selection or an outdoor seal approval.

**ASSUMPTION:** the full M05 rectangular ring contacts uniformly. Its area is `(665*330 - 645*310)/1,000,000 = 0.0195 m2`.

**CALCULATION:** coupon stress times assumed area gives **526.5–1,482 N**, typical 799.5 N, at that test compression. By comparison, the assumed 500 Pa door differential gives about 100 N. These are different loads, not interchangeable. Pressure direction, weight, panel bending and actual force distribution must be considered by the reviewer. Summing published static latch capacities does not establish usable closing force or latch count.

For a hypothetical nominal 3.18 mm sheet, the existing 3 mm gap gives only 5.66% nominal compression. Its thinnest tolerance example is 2.862 mm, so it may not contact at all. A nominal 25% gap would be 2.385 mm; holding that gap across the thickness tolerance produces 16.67–31.82% compression. No force is extrapolated at those strains: obtain the full curve and actual tolerances first. No CAD gap changed.

This arithmetic is not installed seal performance: seams/corners, adhesive, aging, temperature, flatness and cover deflection are absent. Confirm material suitability and leakage separately. Do not transfer material-level environmental claims to the tower.

## Recommended next closure decision

Compare external compression closures that avoid piercing the seal path against through-cover latches with reviewed sealed mounting. A retained cover/captive fastening option can also be reviewed. No option, bolt size, count or material is approved yet.

Before generating another CAD branch, obtain/review: exact latch drawing and catch CAD; usable closing force versus adjustment/travel; gasket profile, free thickness and full force curve; allowed compression and compression stops; flange/cover stiffness and flatness; supported removal/drop retention; tool/hand/lever clearance. Redesign land/locations only after these inputs. HEPA element seating gasket is a separate interface from this access-door gasket.

Six build gates remain open. This step finds a real interface problem; it does not release the previous clash-free CAD for fabrication. No purchase, supplier message, physical test, CFD or CAD alteration performed.

## Reproduce and audit

`python scripts/analysis/hatch_hardware_screen.py`

`python -m unittest discover -s scripts/analysis -p 'hatch_hardware_screen.py'`

Results: `results/fan_selection/hatch_hardware_screen.json`; six unit tests check arithmetic/invalid inputs, NOT physical seals or mechanisms.

Archived PDFs under `data/hardware/sources/` (downloaded 2 October 2026):

- `Southco_C5_review_2026-10-02.pdf`, SHA256 `5670d34926436ad701a235ca72e67c53c48684a360858b8f9a05e19296715c0a`.
- `Rogers_PORON_4701_40_review_2026-10-02.pdf`, SHA256 `f8c30aa093f5df92f5db1f7e7e4ff98b9a20914badc667daac627c1948b32199`.

Source pages were rendered and visually checked to avoid misreading table columns. Renderings are reference snapshots, not new product drawings. Preserve OEM copyright/branding; review redistribution permissions before public publication.
