# D01 R02 — removable experimental filter adapter

**Detail revision:** [R02H fastening and service](hardware_detail/README.md) adds adapter hardware and filter-withdrawal checks to this same assembly. Use its integrated CAD for current hardware review; retain these R02 panel drawings as geometry references. Neither revision is released for manufacture.

3 October2026. Continues the saved R01 cabinet, not a new tower architecture. **Review only: not released for cutting, purchase or energization.** Physical prototypes:0.

## Delivered

- `D01_R02_ASSEMBLY.FCStd`: integrated169-object native assembly.
- `D01_R02_ASSEMBLY.step`: neutral assembly export, volume/reopen checked.
- `D01_R02_ADAPTER_DRAWINGS.pdf`: two sheets, actual CAD render and dimensioned panel/hole layouts.
- `panel_dxf_REVIEW_ONLY/`: two proposed panel drawings, quantity2 each.
- `ADAPTER_DELTA_BOM.csv`: additions/replacements only, NOT a full procurement BOM. Retained R01 hardware is still provisional.
- `checks.json`, `panels.json`, `cad_mesh.json`: reproducible geometry evidence.

The front/rear module replaces the large reference filters, retaining panels and low shelves with a reducing plate, smaller filter gasket, actual-size filter envelope, removable retaining frame and independent support ledges. The original R01 file and hash are preserved. Source uses an analytic mirror; the first trial's generic geometry transform introduced a STEP volume mismatch and was replaced. Final native/STEP checks pass.

## Dimensions and assembly concept

Existing cabinet aperture470 x470; existing gasket495.3 outside/475.3 inside,3mm installed. Adapter550 x550 x9 covers the original opening and contacts that existing gasket. Its opening is350 x270. The new gasket is370 x290 outside/350 x270 inside,3mm installed. Filter envelope370 x290 x40. Retainer410 x330 x9, opening350 x270. The10mm new gasket/retainer bearing border is an **assumption**, not verified OEM frame geometry.

Front stack along global y: cabinet0; existing gasket-3..0; adapter-12..-3; new gasket-15..-12; filter-55..-15; retainer-64..-55. Rear mirrors about y180. New outer retainer-to-retainer depth488mm; proposed new studs extend total depth500mm. Other R01 reservations remain; this is not final shipping size.

Eight existing M5 studs per side retain the adapter. Four new M4 shaft envelopes per side retain the smaller frame. Two bent ledges per side support the filter bottom atz160; retention must not rely on friction alone. New fastener penetrations into the plenum have proposed sealing washer envelopes. Relief holes around inherited seat bolt heads lie outside the original perimeter seal. Neither a drawn gasket nor a drawn sealing washer proves airtightness.

Proposed assembly order, after eventual design release: install ledges on reducer; fit reducer to existing gasket/studs with all feedthrough seals; inspect flatness/contact; fit new gasket; rest filter on ledges; fit retaining frame; secure using reviewed hardware/compression procedure. No tightening torque is specified without actual frame/gasket data. Service requires unplugging and stopping rotation, then removing the small retaining frame while supporting the filter. Exact removal clearances and remaining heads/nuts require a physical fit check. The outer intake remains exposed media, not a vandal guard.

## What is verified, assumed and unknown

**Verified source fact:** [IKEA India104.633.30](https://www.ikea.com/in/en/p/starkvind-filter-for-particle-removal-10463330/) publishes370 x290 x40mm and explicitly intends use only with STARKVIND appliances. This custom integration is experimental and not endorsed or certified by IKEA. No MERV13/HEPA label is attached to our modified unit. Product tolerances, exact sealing border and allowed frame pressure are unknown.

**Digital checks:**169 valid shape objects;5,310 new-to-existing/new-to-new pair checks with no positive-volume clashes above0.05mm3; native reopen and STEP volume match. Inherited R01 pairs were not redundantly rechecked; original guards/reservations and prior limitations persist. Zero nominal clash does not verify strength, safety or tolerance.

Both PDF sheets were rendered and visually inspected. Filter pleats and guard perforations in the illustration are renderer annotations, not detailed CAD geometry. The external controls and cable path are reservations, not released electronics or wiring. Projecting shaft envelopes require final length/retention and snag/impact protection review.

**Assumptions:**9mm plate material thickness,3mm installed gasket,10mm flat filter border, shaft sizes,1mm installed feedthrough seals,2mm sharp-corner bent brackets. Actual panel grade, bracket bend radius/strength, gasket product, seal force, locknuts, washers, heads, exposed-stud protection and fastener retention remain incomplete. The thin reducing panel spans a470mm opening: bending/clamp loading still needs evaluation. The filter is an external solid envelope, not a media/frame detail model.

**Airflow:** do NOT reuse R01 predictions. Two new350x270 openings give0.189m2 combined opening area; at an assumed300m3/h, opening speed is0.441m/s. That is geometry arithmetic, not predicted delivered flow. Filter resistance, reducer losses and leakage require a new budget or measurement. No measured CADR, particle-removal result, gas cleaning or outdoor radius exists.

**Safety:** same unresolved restart protection, electrical startup/current checks, guard access/strength, enclosure and physical commissioning as R01. Not unattended/public/outdoor-ready; the India heat/weather/vandalism requirements remain in `docs/build/INDIA_DEPLOYMENT_BASIS.md`.

The aqi-build-review skill required explicit sealing of adapter fastener paths, separate weight support and withdrawal of inherited airflow predictions. No purchase, installation or supplier contact occurred.

## Reproduce

Run `scripts/geometry/adapt_d01_filter.py` using existing FreeCAD Python, then `scripts/reports/build_d01_adapter_report.py` using existing bundled Python. Uses saved R01 as input, with no change to its native file. This is reproducible explicit-coordinate geometry, not a fully constrained production model.
