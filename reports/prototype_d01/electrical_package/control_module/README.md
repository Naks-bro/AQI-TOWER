# E03 — external control-module body layout

[Dimensioned drawing](D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf), [FreeCAD envelopes](D01_E03_CONTROL_ENVELOPES.FCStd), [STEP envelopes](D01_E03_CONTROL_ENVELOPES.step), [placement coordinates](PLACEMENT.csv), [fit evidence](FIT_CHECKS.json). **Not for drilling, wiring or energization.**

FACT: the40mm tower reservation cannot accommodate the proposed Opta in normal DIN orientation. DETECTED: three OEM-sized body proxies and three assumed service volumes clear the downloaded Hammond STEP, excluding its support panel. Body separations65,85 and47mm. Native493-object tower CAD unchanged; physical prototypes0. **Body fit is not a completed control-panel fit:** PR1, fuse holders, terminals, buttons, actual cables and supports absent; do not assume these will fit the remaining space.

VERIFIED references: Hammond1554XA2GY nominal300x200x120mm, matching1554XPL panel285x185mm; Opta70x88.8mm front/61.1mm depth reservation; Noctua hub93x43x12.5mm, controller21x25x48mm. Panel page rounds thickness to2mm; supplied STEP models1.6256mm. Verify delivered thickness/fastener stack. ASSUMED Opta back at7.5mm rail crest;5mm hub/controller carrier lift, not selected hardware. Magnets alone not accepted installed retention. Reference Phoenix0801733 rail35x7.5mm,15x6.2 slots/25mm pitch; proposed125mm cut and4.5mm rail holes at X-122.5/-22.5,Y0 are NOT drilling release. Recommend obtainable equivalent standard cut piece, not the25-piece/50m catalogue pack. India stock/price UNKNOWN.

Critical finding: NA-FC1 dial/switch cannot be operated through a closed lid here. A reviewed enclosed access arrangement or different component is required. Do not run with an open box. No lid, cable or thermal-vent cutouts released.

## Reproduce / licensing

Use existing FreeCAD bundled Python. Download [exact Hammond STEP ZIP](https://www.hammfg.com/files/parts/stp/1554XA2GY.zip) into local `tmp/control_oem`, extract `1554XA2GY.stp` into `tmp/control_oem/step`, run `scripts/geometry/layout_d01_control_module.py`. Then run `scripts/reports/build_d01_control_layout.py` using the existing report runtime. Checks solid count/panel envelope, intersections and saved/reopened shapes; source hash recorded.

OEMSTEP/PDFs stay ignored local references: redistribution license not established. PublicCAD contains original simplified envelopes, not moulded geometry/panel contour/holes/gasket/threads. Not manufacturing geometry or permission to reproduce the OEM product. Same proposed D01 module, not an alternative tower branch.

Primary sources checked5 October2026:

- [Box drawing, rev28 February2020](https://www.hammfg.com/files/parts/pdf/1554XA2GY.pdf), [box page](https://www.hammfg.com/part/1554XA2GY), [panel drawing, rev1 November2019](https://www.hammfg.com/files/parts/pdf/1554XPL.pdf).
- [Opta datasheet, dimensions page16](https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf).
- [Noctua hub](https://www.noctua.at/en/products/na-fh1/specifications), [speed controller](https://www.noctua.at/en/products/na-fc1/specifications).
- [Phoenix rail](https://www.phoenixcontact.com/en-us/products/din-rail-ns-35-75-perf-2000mm-0801733).

Remaining: selected protection/terminals and their volumes, retained rail/carriers, real entries/bends, closed-lid controls, heat rise, functional earth/metal panel treatment, module placement/retention, tower harness interface. External unmodified adapter stays outside; no mains inside proposal. Qualified acceptance and unpowered fit checks precede dummy-load commissioning. Stock IP68 does not rate our modified assembly; no protective requirement waived.
