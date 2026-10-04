# D01 component evidence and filter duty — 3 October 2026

Same R01 assembly; no new CAD branch. **REVIEW ONLY. Physical prototypes: 0.**

## What changed

Archived the manufacturer's 14-point, 2800 rpm numeric fan curve and reran the complete R01 pressure budget. See `D01_COMPONENT_CHECK.pdf`, `pressure_comparison.json`, `OEM_P14_Max_points.csv`, and `filter_headroom.csv`. Nine calculation checks pass; historical R01 results reproduce. Existing CAD, drawings and historical calculations remain unchanged.

The numeric data give approximately **371 / 344 / 299 m3/h**, versus the previous **359 / 337 / 298 m3/h**, for the same assumed 5 / 10 / 20 Pa filter paths at 400 m3/h total. These are scenarios, NOT measured performance, uncertainty bounds, CADR or outdoor coverage. Both filters are in parallel: each sees half the total flow, and their pressure drops are not added. Four parallel fans add flow, not pressure.

## Real design consequence

Under the current guard/plenum assumptions, **400 m3/h is not supported even before adding filter resistance** by either curve. At a proposed 300 m3/h comparison duty, each filter passes 150 m3/h and has approximately 14.5–14.7 Pa remaining pressure allowance. At 350 total, only 6.2–7.7 Pa remains. These are balance limits with the existing modeled installation allowance, NOT acceptance limits with a validated operating margin. Do not buy an arbitrary MERV13 filter and expect it to work.

Recommendation: compare obtainable filters at **150 and 175 m3/h per element**, with actual clean resistance and loading data. Use 300 total as a provisional procurement comparison point, not a promised output or a user-approved performance requirement. An element exceeding the allowance requires a lower duty or a revised fan/filter/guard combination, not an optimistic report. Guard losses and plenum losses themselves remain assumptions; no guard aperture enlargement is authorized by this calculation.

## Fan evidence: two separate discrepancies

1. Official support downloads identify **ACFAN00287A as black single** and **ACFAN00290A as black five-pack**. However, the archived specification PDF visibly labels 00287A white and 00304A black. The discrepancy is real in that PDF, not merely text-extraction order. An interim chat statement calling it our reading error was premature and is corrected here. Require supplied product label/revision and matching drawing before purchase. `spec_check.png` records the visually checked page.
2. Numeric workbook endpoints are **109.85 CFM / 4.487 mmH2O**, whereas the brochure lists **95 CFM / 4.18 mmH2O**. The separate 2024 PQ graph is also labeled 2800 rpm. No explanation of the different test/revision basis was obtained. Keep both analyses; do not average them or assert the larger result is guaranteed. Workbook header `C=0.95` is preserved; its meaning is unconfirmed and no second correction was applied. The workbook's actual numeric cells, not formula outputs, were extracted without modifying the source.

## Filter research disposition

- **S&P 990303** remains the R01 dimensional reference (495.3 x495.3 x44.45 mm), not an obtainable, pressure-qualified selection. Exact low-flow resistance, frame tolerances, seal landing and India supply remain UNKNOWN.
- **Camfil AQ13 407051002** is an OEM-listed nominal 20x20x2 inch MERV13/11A candidate in the 2025 sheet. This is NOT a confirmed drop-in substitute: the current sheet lists nominal sizes but does not supply the actual dimensions or a usable low-flow pressure curve. No resistance figure from an older AQ13 variant has been transferred to it. MERV13/11A does not establish whole-device efficiency or HEPA performance.
- Camfil has an official India contact route. This proves a route for an inquiry, not availability of this US-listed SKU, price, delivery date or supply commitment. No inquiry was sent. The other searched nominal sizes/classes do not establish a compatible D01 part.

The useful next external input is one exact filter offer with drawing, per-element pressure curve spanning 125–200 m3/h, loading/replacement information, mass, seal landing and delivered quote. This is the component-selection blocker; more cosmetic CAD cannot close it. Do not cut the filter seats until the exact frame and sealing interface are confirmed.

## Sources and provenance

Accessed 2026-10-03. Manufacturer documents are evidence, not openly licensed product designs; no open-source licence or patent right is inferred. Archived locally for project review; do not redistribute OEM files as our work.

- [ARCTIC official documentation and black SKU declarations](https://support.arctic.de/p14-max/docs)
- [Numeric PQ workbook](https://support.arctic.de/products/p14-max/techdocs/P14%20Max%20-%20PQ%20Curve%20for%20CFD.XLSX), archived `data/prototype_d01/sources/ARCTIC_P14_Max_PQ_CFD.xlsx`; hash in results JSON.
- [Separate PQ graph](https://support.arctic.de/products/p14-max/techdocs/20240919_P14%20Max%20-%20PQ%20curve.pdf), archived `ARCTIC_P14_Max_PQ_20240919.pdf`.
- [ARCTIC specification PDF](https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf), previously archived `ARCTIC_P14_Max_Spec.pdf`.
- [Camfil AQ13 2025 sheet](https://www.camfil.com/dam/files/682/1671789/Product-Sheet-AQ13.pdf.pdf), archived `Camfil_AQ13_2025.pdf`.
- [Camfil India contact locator](https://www.camfil.com/en-in/support-and-services/support/contact-locator).

## Release boundary and reproduction

The aqi-build-review skill required source discrepancies to remain visible and all losses to be compared at the same flow. Geometry, electrical/current/startup/restart protection, structural/guard/seal review and physical commissioning gates remain open. No ordering, supplier contact, installation, wiring or physical testing occurred.

Run `scripts/analysis/d01_oem_curve_check.py`, then `scripts/reports/build_d01_component_check.py` with the existing bundled Python. The second script builds the two-page review PDF, renders its pages and records source/output hashes. Calculation uses linear interpolation between OEM points; equal fan/filter sharing, no bypass, full 2800 rpm and all existing R01 system-loss assumptions remain unverified. No source workbook is saved or altered.
